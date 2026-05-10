"""Runner — pipes generator output through RacketBridge to produce
validated (input, output) pairs.

Two source-level conversions are required before sending a rule to
RacketBridge:
  - Strip `;` line comments. The bridge flattens newlines to spaces
    when sending to Racket; a comment that survives the flatten will
    eat the entire rest of the rule.
  - Replace `{K V K V ...}` dict literals with
    `(make-immutable-hash (list (cons K V) ...))`. The executor does
    this in `_expr_to_text`; the bare bridge does not.

The runner is the only place generators meet Racket. It owns:
  - Loading the puzzle's rule from data/base/solutions/<task_id>.
  - Wrapping the rule body so it becomes a callable Racket function
    (mirroring what arc_repl.executor._handle_rule does).
  - Spinning a persistent RacketBridge per batch (cold-start
    amortization: ~150ms once vs ~150ms per call).
  - Validating each (input, output) pair.
  - Writing rejected instances to data/generated/.rejected/<task_id>.jsonl.
  - Bundling validated pairs into {train: [...], test: [...]} dicts.

Public entry points:
    run_one(task_id, seed, sample_index, *, n_train=4, n_test=1, **axes)
    run_batch(task_id, n, *, n_train=4, n_test=1, max_retries=3, **axes)

Phase 2.3 of docs/PUZZLE_GENERATOR_ROADMAP.md.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from arc_repl.racket_bridge import RacketBridge, RacketBridgeError  # noqa: E402

from puzzle_generators.helpers.grid import is_well_formed  # noqa: E402

# Rule-source normalization (strip comments, dict literals, for shorthand,
# rule! peel, h/w preamble). Owned by puzzle_generators.rule_wrap so the
# compactor verifier and ad-hoc tooling can import the same pipeline
# without dragging in the rest of the runner.
from puzzle_generators.rule_wrap import wrap_rule  # noqa: E402,F401

SOLUTIONS_DIR = ROOT / "data" / "base" / "solutions"
REJECT_DIR = ROOT / "data" / "generated" / ".rejected"


def _parens_balanced(code: str) -> bool:
    """Quick balance check for Racket source. Handles () [] plus line
    comments and string literals. Conservative: false if anything is
    suspicious.

    Inlined from scripts/comment_solutions.py so the runner has no
    dependency on the scripts package — this matters when the bundle
    is shipped without the full repo."""
    depth = 0
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        if c == ";":
            while i < n and code[i] != "\n":
                i += 1
            continue
        if c == '"':
            i += 1
            while i < n and code[i] != '"':
                i += 2 if code[i] == "\\" else 1
            i = min(i + 1, n)
            continue
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0


def _load_rule(task_id: str) -> tuple[str, str]:
    """Find a usable rule for `task_id` and return (rule_source, source_label).

    Resolution order:
      1. `data/base/solutions/banks/.../*.json` (preferred — gives a
         file path label and supports augmented-variant overrides).
      2. `solvers.grounded_rules.GROUNDED_RULES[task_id]` (fallback —
         used when the rule-source data dir is absent, e.g. a stripped
         review bundle that only ships generators + grounded_rules).

    Multiple JSON solution files can exist for one task_id (training +
    augmented variants). We pick the first one with a non-empty,
    paren-balanced racket_target."""
    if SOLUTIONS_DIR.exists():
        for f in sorted(SOLUTIONS_DIR.rglob("*.json")):
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            if d.get("task_id") != task_id:
                continue
            rt = d.get("racket_target") or {}
            if rt.get("needs_conversion"):
                continue
            src = rt.get("target_code") or rt.get("raw_code") or ""
            src = src.strip()
            if not src or not _parens_balanced(src):
                continue
            return src, str(f.relative_to(ROOT))
    # Fallback: solvers/grounded_rules.py.
    try:
        from solvers.grounded_rules import GROUNDED_RULES
    except Exception:
        GROUNDED_RULES = {}
    rule = GROUNDED_RULES.get(task_id)
    if rule:
        rule = rule.strip()
        if rule and _parens_balanced(rule):
            return rule, "solvers.grounded_rules"
    raise FileNotFoundError(
        f"no usable rule found for task_id {task_id} "
        f"(checked data/base/solutions/ and solvers/grounded_rules.py)")


# ---------------------------------------------------------------------------
# Generator loading
# ---------------------------------------------------------------------------

def _load_generator_module(task_id: str):
    """Import puzzle_generators.per_puzzle.<task_id>.generator. The
    task_id is the per-puzzle directory name (a 12-char content_hash)."""
    full = f"puzzle_generators.per_puzzle.{task_id}.generator"
    try:
        return importlib.import_module(full)
    except ModuleNotFoundError as e:
        raise FileNotFoundError(
            f"no generator module for task_id {task_id} "
            f"(expected puzzle_generators/per_puzzle/{task_id}/generator.py)"
        ) from e


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

@dataclass
class Rejection:
    """Why an attempt was rejected. The `reason` is a phase-prefixed
    short tag like 'generate.generator_raised', 'execute.rule_raised',
    'validate.duplicate_pair'. `detail` is a small dict of structured
    context — exception class, dims, hash, etc. Keep payloads small;
    these get persisted line-by-line to the rejection log.

    Phase prefixes:
      generate.* — driver called bundle.generator_module.generate(...)
      execute.*  — Racket bridge applied the rule
      validate.* — well-formedness + identity + dedup checks
    """
    seed: int
    sample_index: int
    reason: str
    detail: dict = field(default_factory=dict)


# Mapping from pre-round-4 unprefixed reason strings to their
# phase-prefixed equivalents. Used by `normalize_rejection_row` for
# tolerant reads of legacy `data/generated/.rejected/<id>.jsonl` lines.
_LEGACY_REASON_MAP = {
    "generator_raised":      "generate.generator_raised",
    "input_not_well_formed": "generate.input_not_well_formed",
    "rule_raised":           "execute.rule_raised",
    "output_not_well_formed": "validate.output_not_well_formed",
    "output_equals_input":   "validate.output_equals_input",
    "duplicate_pair":        "validate.duplicate_pair",
}


def normalize_rejection_row(row: dict) -> dict:
    """Tolerant read of a single rejection-log line.

    Pre-round-4 logs had unprefixed `reason` strings and a `detail`
    that was either a string or absent. Round 4 switched to
    phase-prefixed reasons and dict details. Aggregators and
    diagnostic tools should pipe each row through this normalizer so
    they don't need to special-case the schema break.
    """
    reason = row.get("reason", "")
    if "." not in reason:
        reason = _LEGACY_REASON_MAP.get(reason,
                                         f"legacy.{reason}" if reason else "legacy.unknown")
    detail = row.get("detail", {})
    if isinstance(detail, str):
        detail = {"message": detail} if detail else {}
    elif detail is None:
        detail = {}
    return {**row, "reason": reason, "detail": detail}


def _content_hash(grid_pair: dict) -> str:
    """Stable hash of an (input, output) pair for dedup."""
    blob = json.dumps([grid_pair["input"], grid_pair.get("output", [])],
                      ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


def _validate_pair(inp, out, *, allow_identity_output: bool) -> Optional[str]:
    """Return None if valid, otherwise a phase-prefixed rejection reason.

    Conservative: only reject what's clearly degenerate. A uniform-color
    output is *legitimate* for many rules (`crop-object` returns a
    monochrome rectangle, `extract-largest` likewise) — we don't flag it."""
    if not is_well_formed(inp):
        return "validate.input_not_well_formed"
    if not is_well_formed(out):
        return "validate.output_not_well_formed"
    if not allow_identity_output and inp == out:
        return "validate.output_equals_input"
    return None


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

@dataclass
class GeneratorBundle:
    """What the runner loads once per batch. Reused across all instances."""
    task_id: str
    rule_source: str
    rule_callable_text: str            # the (lambda (g) ...) string
    rule_file: str
    generator_module: Any
    allow_identity_output: bool = False


def _load_bundle(task_id: str) -> GeneratorBundle:
    rule_src, rule_file = _load_rule(task_id)
    callable_text = wrap_rule(rule_src)
    mod = _load_generator_module(task_id)
    # Check for opt-in identity flag in meta.yaml (lightweight: read .meta_allows_identity)
    allow_id = bool(getattr(mod, "ALLOW_IDENTITY_OUTPUT", False))
    return GeneratorBundle(
        task_id=task_id,
        rule_source=rule_src,
        rule_callable_text=callable_text,
        rule_file=rule_file,
        generator_module=mod,
        allow_identity_output=allow_id,
    )


def _open_bridge_with_rule(rule_callable_text: str) -> tuple[RacketBridge, str]:
    """Spin a bridge and pre-define the rule as a named function.
    Returns (bridge, function_name) — caller invokes via
    `(<function_name> <input>)`."""
    b = RacketBridge()
    fn_name = "__pg_rule"
    b.eval_text(f"(define {fn_name} {rule_callable_text})")
    return b, fn_name


def _apply_rule(bridge: RacketBridge, fn_name: str, input_grid) -> list:
    """Define the input grid and call the rule. Returns the output grid."""
    bridge.define_grid("__pg_input", input_grid)
    return bridge.eval_text(f"({fn_name} __pg_input)")


def run_one(
    task_id: str,
    seed: int,
    sample_index: int,
    *,
    n_train: int = 4,
    n_test: int = 1,
    bundle: Optional[GeneratorBundle] = None,
    bridge: Optional[RacketBridge] = None,
    fn_name: Optional[str] = None,
    **axes,
) -> dict:
    """Build one puzzle instance: n_train + n_test (input, output) pairs.

    All pairs in the instance share a seed root and use sequential
    sample_indices starting from `sample_index`."""
    bundle = bundle or _load_bundle(task_id)
    if bridge is None:
        bridge, fn_name = _open_bridge_with_rule(bundle.rule_callable_text)

    rejections: list[Rejection] = []
    pairs: list[dict] = []
    seen_hashes: set[str] = set()
    si = sample_index
    needed = n_train + n_test
    max_attempts = needed * 5  # 5x slack before giving up
    attempts = 0
    while len(pairs) < needed and attempts < max_attempts:
        attempts += 1
        try:
            inp = bundle.generator_module.generate(
                seed=seed, sample_index=si, **axes)
        except Exception as e:
            rejections.append(Rejection(seed, si, "generate.generator_raised",
                                         {"exception_class": type(e).__name__,
                                          "message": str(e)[:200]}))
            si += 1
            continue
        if not is_well_formed(inp):
            rejections.append(Rejection(seed, si, "generate.input_not_well_formed",
                                         {"rows": len(inp),
                                          "cols": len(inp[0]) if inp else 0}))
            si += 1
            continue
        try:
            out = _apply_rule(bridge, fn_name, inp)
        except RacketBridgeError as e:
            rejections.append(Rejection(seed, si, "execute.rule_raised",
                                         {"message": str(e)[:200]}))
            si += 1
            continue
        reason = _validate_pair(inp, out,
                                 allow_identity_output=bundle.allow_identity_output)
        if reason:
            rejections.append(Rejection(seed, si, reason, {}))
            si += 1
            continue
        pair = {"input": inp, "output": out}
        h = _content_hash(pair)
        if h in seen_hashes:
            rejections.append(Rejection(seed, si, "validate.duplicate_pair",
                                         {"content_hash": h}))
            si += 1
            continue
        seen_hashes.add(h)
        pairs.append(pair)
        si += 1

    if len(pairs) < needed:
        # Persistent under-production — write the rejection log so the
        # generator's flaws are visible.
        _record_rejections(task_id, seed, rejections)
        raise RuntimeError(
            f"run_one({task_id}, seed={seed}): only produced "
            f"{len(pairs)}/{needed} valid pairs after {attempts} attempts. "
            f"See {REJECT_DIR}/{task_id}.jsonl")

    return {
        "task_id": task_id,
        "seed":    seed,
        "train":   pairs[:n_train],
        "test":    pairs[n_train:],
    }


def run_batch(
    task_id: str,
    n: int,
    *,
    n_train: int = 4,
    n_test: int = 1,
    seed_start: int = 0,
    **axes,
) -> list[dict]:
    """Build n independent puzzle instances. Each gets its own seed."""
    bundle = _load_bundle(task_id)
    bridge, fn_name = _open_bridge_with_rule(bundle.rule_callable_text)
    out = []
    try:
        for i in range(n):
            inst = run_one(
                task_id,
                seed=seed_start + i,
                sample_index=0,
                n_train=n_train, n_test=n_test,
                bundle=bundle, bridge=bridge, fn_name=fn_name,
                **axes,
            )
            out.append(inst)
    finally:
        bridge.shutdown()
    return out


def _record_rejections(task_id: str, seed: int, rejections: Iterable[Rejection]) -> None:
    REJECT_DIR.mkdir(parents=True, exist_ok=True)
    p = REJECT_DIR / f"{task_id}.jsonl"
    with p.open("a") as f:
        for r in rejections:
            f.write(json.dumps({
                "task_id": task_id, "seed": r.seed,
                "sample_index": r.sample_index,
                "reason": r.reason, "detail": r.detail,
            }, ensure_ascii=False) + "\n")
