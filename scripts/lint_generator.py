#!/usr/bin/env python3
"""Static lint for a candidate puzzle-instance generator.

Use case: an offline-authored generator (paste into ChatGPT / etc., get
a Python file back) needs a sanity check before being committed. This
script validates the file against the spec WITHOUT running it. Call
with `--validate` to also run 20 instances through the runner.

Usage:
    # Lint a file at a specific path:
    python3 scripts/lint_generator.py path/to/generator.py

    # Lint by task_id (resolves to puzzle_generators/per_puzzle/<id>/generator.py):
    python3 scripts/lint_generator.py 952a094c

    # Also actually run the generator:
    python3 scripts/lint_generator.py 952a094c --validate

Checks:
  1. File parses as Python.
  2. Required module constants present and well-typed:
     GENERATOR_ID, VERSION, TASK_ID, CONCEPT_HASH, SUMMARY,
     INVARIANTS (non-empty list[str]), AXES (dict).
  3. TASK_ID matches dirname (with `:` ↔ `__` mangling).
  4. CONCEPT_HASH matches the canonicalized rule (warning if mismatched).
  5. Has `def generate(seed, sample_index, *, difficulty=None, **overrides)`.
  6. No `import random` or bare `random.*` calls (use ctx.draw_*).
  7. No suspicious "rule reimplementation": rule's primitive heads
     (find-color, recolor, etc.) appearing as Python function names is
     a smell — likely the model translated the rule into Python.
  8. Returns from `generate` exit type-compatible (return statements
     present, not just falling off end).

Exit codes:
  0 — all checks pass
  1 — at least one warning (yellow) but nothing fatal
  2 — at least one error (red) — do not integrate
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PER_PUZZLE_DIR = ROOT / "puzzle_generators" / "per_puzzle"

GREEN = "\033[32m"; RED = "\033[31m"; YELLOW = "\033[33m"; RESET = "\033[0m"


# Heads from the Racket prelude that, if they appear as Python identifiers,
# suggest the author tried to translate the rule into Python instead of
# using the bridge. Soft signal — emit a warning, not a fatal error.
RACKET_PRIMITIVE_NAMES = {
    "find_color", "find-color", "recolor", "objects", "objects_8",
    "obj_color", "obj_size", "obj_bbox", "obj_cells", "crop_to_content",
    "self_tile", "kaleidoscope", "rotate_cw", "flip_lr",
}


class LintReport:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def err(self, msg: str): self.errors.append(msg)
    def warn(self, msg: str): self.warnings.append(msg)
    def note(self, msg: str): self.notes.append(msg)

    @property
    def exit_code(self) -> int:
        if self.errors: return 2
        if self.warnings: return 1
        return 0


def lint_generator(path: Path, *, validate: bool = False) -> LintReport:
    r = LintReport()
    if not path.exists():
        r.err(f"file not found: {path}")
        return r

    src = path.read_text()

    # 1. Parses as Python
    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError as e:
        r.err(f"Python syntax error: {e}")
        return r

    # 2. Required module constants
    constants: dict[str, object] = {}
    has_generate = False
    generate_node = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    try:
                        constants[tgt.id] = ast.literal_eval(node.value)
                    except Exception:
                        constants[tgt.id] = "<non-literal>"
        elif isinstance(node, ast.FunctionDef) and node.name == "generate":
            has_generate = True
            generate_node = node

    required = {
        "GENERATOR_ID":  str,
        "VERSION":       str,
        "TASK_ID":       str,
        "SUMMARY":       str,
        "INVARIANTS":    list,
        "AXES":          dict,
    }
    optional = {
        # CONCEPT_HASH was once required; now optional. Round-7 audit
        # found 1356/2616 generators shipped CONCEPT_HASH = "" (empty)
        # which is worse than absent because it looks filled. Treat
        # empty as "not yet computed" (warn), absent as "not relevant".
        "CONCEPT_HASH":  str,
    }
    for name, t in required.items():
        if name not in constants:
            r.err(f"missing required module constant: {name}")
        elif constants[name] == "<non-literal>":
            r.warn(f"{name} is not a literal — can't validate type")
        elif not isinstance(constants[name], t):
            r.err(f"{name} should be {t.__name__}, got {type(constants[name]).__name__}")
        elif t is list and not constants[name]:
            r.err(f"INVARIANTS must be a non-empty list of strings")
        elif t is dict and not constants[name]:
            r.warn(f"AXES is empty — generator has no documented free parameters")
    for name, t in optional.items():
        if name in constants:
            v = constants[name]
            if v == "<non-literal>":
                r.warn(f"{name} is not a literal — can't validate type")
            elif not isinstance(v, t):
                r.warn(f"{name} should be {t.__name__}, got {type(v).__name__}")
            elif t is str and v == "":
                r.warn(f"{name} is empty string — refresh via "
                       f"scripts/concept_inventory.py or remove the constant")

    # 3. TASK_ID matches dirname
    task_id = constants.get("TASK_ID", "")
    if isinstance(task_id, str):
        expected_dir = task_id.replace(":", "__").replace("/", "__").replace("-", "_")
        # Determine the candidate dirname from the file's parent
        if path.parent.name != expected_dir and path.parent.parent == PER_PUZZLE_DIR:
            r.err(f"TASK_ID={task_id!r} but file is in directory "
                   f"{path.parent.name!r} (expected {expected_dir!r})")

    # 4. CONCEPT_HASH matches canonicalized rule
    if isinstance(task_id, str) and task_id:
        try:
            from puzzle_generators.runner import _load_rule
            from scripts.canonicalize_rule import canonicalize_rule
            rule_src, _ = _load_rule(task_id)
            info = canonicalize_rule(rule_src)
            real_hash = info.get("concept_hash")
            claimed = constants.get("CONCEPT_HASH")
            if real_hash and claimed and claimed != real_hash:
                r.warn(f"CONCEPT_HASH mismatch: claimed {claimed!r}, actual {real_hash!r}")
        except Exception as e:
            r.note(f"could not canonicalize rule for verification: {e}")

    # 5. generate signature
    if not has_generate:
        r.err("missing required function: generate(...)")
    else:
        args = generate_node.args
        # Required positional: seed, sample_index
        pos = [a.arg for a in args.args]
        if pos[:2] != ["seed", "sample_index"]:
            r.err(f"generate() should start with positional args (seed, sample_index), got {pos}")
        # difficulty must be keyword-only
        kw_args = [a.arg for a in args.kwonlyargs]
        if "difficulty" not in kw_args:
            r.warn("generate() should accept `difficulty` as a keyword-only arg")
        if args.kwarg is None or args.kwarg.arg != "overrides":
            r.warn("generate() should accept `**overrides`")

    # 6. No bare random.* usage
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name == "random":
                    r.err("`import random` not allowed — use ctx.draw_rng(label) instead")
        if isinstance(node, ast.ImportFrom) and node.module == "random":
            r.err("`from random import …` not allowed — use ctx.draw_rng(label)")

    # 7. Smell: rule-primitive names appearing as Python identifiers
    # Walk both Name references and FunctionDef.name so we catch both
    # `find_color = ...` and `def find_color(...)`.
    py_names: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            py_names.add(n.id)
        elif isinstance(n, ast.FunctionDef):
            py_names.add(n.name)
    for n in py_names & RACKET_PRIMITIVE_NAMES:
        r.warn(f"identifier `{n}` echoes a Racket primitive — "
               f"are you reimplementing the rule? You shouldn't.")

    # 8. generate() must have at least one return
    if generate_node is not None:
        if not any(isinstance(n, ast.Return) for n in ast.walk(generate_node)):
            r.err("generate() never executes a `return` — must return a grid")

    # 9. Optional: actually run validation
    if validate and not r.errors:
        try:
            from puzzle_generators.runner import run_batch
            batch = run_batch(task_id, n=20, n_train=4, n_test=1)
            pass_n = len(batch)
            if pass_n >= 18:
                r.note(f"validation: {pass_n}/20 instances passed")
            elif pass_n >= 10:
                r.warn(f"validation: only {pass_n}/20 instances passed")
            else:
                r.err(f"validation FAILED: only {pass_n}/20 instances passed")
        except Exception as e:
            r.err(f"validation crashed: {type(e).__name__}: {e}")

    return r


def _print(r: LintReport, path: Path) -> None:
    if r.errors:
        for m in r.errors: print(f"  {RED}ERR {RESET}{m}")
    if r.warnings:
        for m in r.warnings: print(f"  {YELLOW}WARN{RESET}{m}")
    if r.notes:
        for m in r.notes: print(f"  {GREEN}NOTE{RESET}{m}")
    if not (r.errors or r.warnings):
        print(f"  {GREEN}OK  {RESET}all checks passed")
    print(f"\n{path}: {len(r.errors)} error(s), {len(r.warnings)} warning(s), "
          f"exit {r.exit_code}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", help="Path to generator.py or a task_id")
    ap.add_argument("--validate", action="store_true",
                    help="Also run 20 instances through the runner")
    args = ap.parse_args()

    # Resolve target → path
    p = Path(args.target)
    if not p.exists() and not args.target.endswith(".py"):
        # treat as task_id
        d = PER_PUZZLE_DIR / args.target.replace(":", "__").replace("/", "__").replace("-", "_")
        p = d / "generator.py"

    print(f"linting {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}")
    r = lint_generator(p, validate=args.validate)
    _print(r, p)
    return r.exit_code


if __name__ == "__main__":
    sys.exit(main())
