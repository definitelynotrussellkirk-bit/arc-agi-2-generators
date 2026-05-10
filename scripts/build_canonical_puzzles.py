"""Build the canonical puzzles+solutions dataset.

Combines, for every task we have both data and a solver for:
  - the puzzle itself (train pairs + optional test pairs with outputs)
  - the program solution (Racket `(rule! …)` S-expression)
  - any side-car metadata useful for later ranking (difficulty, pattern)

Three sections are written:
  1. `training`  — 1000 ARC training tasks whose task_id has a grounded
                   rule in `solvers/grounded_rules.py`. Carries
                   {train, test (with solutions), program_solution}.
  2. `augmented` — 461 augmented-variant tasks under
                   `data/augmented/augmented_<id>.json` (scrambled +
                   expanded training pairs, no test slot) + rule.
  3. `custom`    — 30 hand-authored tasks under
                   `data/custom_puzzles/all_tasks_hashed.json`.
                   Task_ids are 8-char hashes (ARC-style). Each carries
                   `difficulty` + `pattern` fields for later ranking.
                   Tasks without train+test pairs are included as
                   rule-only templates (n_train=0).

Output: `data/canonical/puzzles.jsonl`
One JSON object per line (streaming-friendly, easy to send/append).

Run:
    python3 scripts/build_canonical_puzzles.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solvers.grounded_rules import GROUNDED_RULES

# Standalone-task descriptions extracted from grounded_rules.py comments.
# Lets training/augmented sections populate `written_solution` from the
# inline comment block authors wrote next to each rule. See
# scripts/extract_standalone_descriptions.py.
_STANDALONE_DESC_PATH = Path(__file__).resolve().parent.parent / "data" / "standalone_descriptions.json"
_STANDALONE_DESCRIPTIONS = {}
if _STANDALONE_DESC_PATH.exists():
    try:
        _STANDALONE_DESCRIPTIONS = json.loads(_STANDALONE_DESC_PATH.read_text())
    except Exception:
        _STANDALONE_DESCRIPTIONS = {}
sys.path.insert(0, str(ROOT / "scripts"))
from puzzle_ids import compute_puzzle_ids, content_hash

DATA = ROOT / "data" / "raw"
AUG_DIR = ROOT / "data" / "augmented"
CUSTOM_DIR = ROOT / "data" / "custom_puzzles"
BANKS_DIR = CUSTOM_DIR / "banks"
OUT_DIR = ROOT / "data" / "canonical"
OUT_PATH = OUT_DIR / "puzzles.jsonl"
BACKLOG_DIR = ROOT / "data" / "derived"
BACKLOG_PATH = BACKLOG_DIR / "conversion_backlog.jsonl"


def _extract_python_function(source: str, name: str) -> str:
    """Return the full `def <name>(...)` block from `source`, or ''
    if not found. Stops at the next top-level `def ` or end-of-file.
    """
    import re
    if not name or not source:
        return ""
    lines = source.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^def {re.escape(name)}\s*\(", line):
            start = i
            break
    if start is None:
        return ""
    # Find next top-level def/class or EOF
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith(("def ", "class ")):
            end = j
            break
    return "".join(lines[start:end]).rstrip() + "\n"


def _normalize_bank_entries(raw) -> list[dict]:
    """Banks ship with one of three top-level wrappers:
      - list[dict]                                          (v0_original, additional_bank, v3_rich_schema)
      - {'meta': {...}, 'puzzles': [...]}                   (v2_meta_puzzles, additional_scaffolded)
      - {task_id: {...}, task_id: {...}}                    (v1_e_m_h_keys)
    Return a flat list of per-puzzle dicts regardless.
    """
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if "puzzles" in raw:
            val = raw["puzzles"]
            if isinstance(val, dict):
                return list(val.values())
            return list(val or [])
        # dict-keyed: task_id → entry
        return list(raw.values())
    return []


def _bank_entry_to_canonical(entry: dict, bank_name: str,
                             sol_src: str) -> tuple[dict, dict] | None:
    """Universal adapter: take one puzzle (any schema) and return
    `(canonical_record, backlog_record_or_None)`. Returns None if the
    entry has no train pairs at all and no solution we can extract.

    Reads bank-side aliases (`name`/`title`, `tags`/`skills`,
    `written_rule`/`written_solution`/`staged_hint`,
    `program_solution`/`reference_program`/`program_source`,
    `program_function`/`solver_name`/`program_name`,
    `test`/`test_input`+`test_output`) and emits canonical names ONLY.
    Python source is kicked out of canonical entirely — a parallel
    backlog row is returned so the work-to-convert is tracked.
    """
    if not isinstance(entry, dict):
        return None
    task_id = entry.get("id") or entry.get("task_id") or ""
    if not task_id:
        return None

    title = entry.get("title") or entry.get("name") or ""

    written = (entry.get("written_solution")
               or entry.get("written_rule")
               or entry.get("staged_hint")
               or "")

    skills = entry.get("skills") or entry.get("tags") or []
    if not isinstance(skills, list):
        skills = [skills]

    train = entry.get("train") or []

    if entry.get("test"):
        test = entry["test"]
    elif entry.get("test_input") is not None:
        test = [{
            "input": entry.get("test_input"),
            "output": entry.get("test_output"),
        }]
    else:
        test = []

    # Solution payload — three shapes upstream:
    #   1. inline code in program_solution / reference_program / program_source
    #   2. a function name pointing at solutions.py
    #   3. nothing executable, just a `written_*` description (pseudocode banks)
    prog_inline = (entry.get("program_solution")
                   or entry.get("reference_program")
                   or entry.get("program_source")
                   or "")
    prog_fn_name = (entry.get("solver_name")
                    or entry.get("program_function")
                    or entry.get("program_name")
                    or "")
    prog_src = prog_inline
    if not prog_src and prog_fn_name:
        prog_src = _extract_python_function(sol_src, prog_fn_name)

    explicit_lang = str(entry.get("program_language", "")).lower()
    is_racket = (explicit_lang == "racket"
                 or prog_src.lstrip().startswith("(rule!"))

    if not prog_src and not written:
        # No solution code AND no written description — nothing to do.
        return None

    racket_text = prog_src if is_racket else ""
    needs_conversion = not bool(racket_text)

    record = {
        "task_id": f"{bank_name}:{task_id}",
        "source": f"bank:{bank_name}",
        "bank": bank_name,
        "original_id": task_id,
        "title": title,
        "difficulty": str(entry.get("difficulty", "")).lower(),
        "skills": skills,
        "written_solution": written,
        "train": train,
        "test": test,
        "program_solution": racket_text,
        "solution_language": "racket",
        "needs_conversion": needs_conversion,
    }

    backlog = None
    if needs_conversion:
        backlog = {
            "task_id": record["task_id"],
            "source": record["source"],
            "bank": bank_name,
            "original_id": task_id,
            "title": title,
            "written_solution": written,
            "function_name": prog_fn_name,
            "python_source": prog_src,
        }
    return record, backlog


def walk_banks(out, backlog_out) -> tuple[int, int, int]:
    """Iterate every banks/<name>/ directory, normalize its puzzles,
    write one canonical line per puzzle and one backlog line per
    not-yet-converted puzzle. Returns
    `(n_written, n_skipped, n_backlogged)`.
    """
    n_written = 0
    n_skipped = 0
    n_backlogged = 0
    if not BANKS_DIR.is_dir():
        return 0, 0, 0
    for bank_dir in sorted(p for p in BANKS_DIR.iterdir() if p.is_dir()):
        bank_name = bank_dir.name
        puzzles_path = bank_dir / "puzzles.json"
        sol_path = bank_dir / "solutions.py"
        if not puzzles_path.exists():
            continue
        raw = load_json(puzzles_path)
        sol_src = sol_path.read_text() if sol_path.exists() else ""
        entries = _normalize_bank_entries(raw)
        for e in entries:
            converted = _bank_entry_to_canonical(e, bank_name, sol_src)
            if converted is None:
                n_skipped += 1
                continue
            rec, backlog = converted
            _emit(out, rec)
            n_written += 1
            if backlog is not None:
                backlog_out.write(json.dumps(backlog) + "\n")
                n_backlogged += 1
    return n_written, n_skipped, n_backlogged


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


_TRAINING_HASH_BY_TID: dict[str, str] = {}
_BUFFER: list[dict] = []


def _emit(out, record: dict) -> None:
    """Stamp content_hash + slug (+ parent_hash when inferable) onto the
    record and buffer it. `out` is ignored — actual writing happens in
    `_finalize` after all rows are seen, so collision-resolved task_ids
    can be assigned in a single deterministic pass.

    parent_hash rules:
      - augmented : parent = training row with the same task_id
      - other sources : parent = None (it's an original)
    """
    ch, slug = compute_puzzle_ids(record)
    record["content_hash"] = ch
    record["slug"] = slug

    source = record.get("source", "")
    parent_hash = None
    parent_reason = None
    if source == "training":
        _TRAINING_HASH_BY_TID[record["task_id"]] = ch
    elif source == "augmented":
        p = _TRAINING_HASH_BY_TID.get(record["task_id"])
        if p:
            parent_hash = p
            parent_reason = "augmented_variant_of_training_task"
    record["parent_hash"] = parent_hash
    record["parent_reason"] = parent_reason
    _BUFFER.append(record)


def _finalize(out) -> None:
    """Apply task_id rename (legacy → content_hash) and write all
    buffered records.

    Rules:
      - Primary rows (parent_hash=None): new_task_id := content_hash;
        if multiple primaries collide on content_hash, suffix _2/_3/...
        in alphabetical-task_id order.
      - Augmented rows: inherit primary's new_task_id by parent_hash
        lookup (so all variants of the same task share one task_id).
    """
    from collections import defaultdict

    primaries = [r for r in _BUFFER if r.get("parent_hash") is None]
    augmented = [r for r in _BUFFER if r.get("parent_hash") is not None]

    # Group primaries by content_hash → resolve collisions
    by_hash = defaultdict(list)
    for r in primaries:
        by_hash[r["content_hash"]].append(r)

    primary_new_id = {}  # old_task_id → new_task_id
    hash_to_new = {}     # content_hash → new_task_id of FIRST primary (for augmented lookup)
    for ch, group in by_hash.items():
        group_sorted = sorted(group, key=lambda r: r["task_id"])
        for i, r in enumerate(group_sorted):
            new_tid = ch if i == 0 else f"{ch}_{i+1}"
            primary_new_id[r["task_id"]] = new_tid
            if i == 0:
                hash_to_new[ch] = new_tid

    # Write all rows with new task_ids — content_hash is THE task_id;
    # no legacy field is emitted.
    for r in _BUFFER:
        old_tid = r["task_id"]
        if r.get("parent_hash") is None:
            new_tid = primary_new_id[old_tid]
        else:
            new_tid = hash_to_new.get(r["parent_hash"], r["content_hash"])
        ordered = {"task_id": new_tid}
        for k, v in r.items():
            if k != "task_id":
                ordered[k] = v
        out.write(json.dumps(ordered) + "\n")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKLOG_DIR.mkdir(parents=True, exist_ok=True)

    train_ch = load_json(DATA / "arc-agi_training_challenges.json")
    train_sol = load_json(DATA / "arc-agi_training_solutions.json")

    n_training = 0
    n_augmented = 0
    n_custom_bank = 0
    n_missing_rule = 0
    n_missing_solution = 0
    n_backlogged = 0

    with OUT_PATH.open("w") as out, BACKLOG_PATH.open("w") as backlog_out:
        # Section 1: canonical training set with solutions
        # GROUNDED_RULES is keyed by content_hash (post-rename), so we
        # compute the hash from grids first, then look up the rule.
        for task_id, task in sorted(train_ch.items()):
            solutions = train_sol.get(task_id)
            if solutions is None:
                n_missing_solution += 1
                continue
            test_with_sol = []
            for i, t in enumerate(task.get("test", [])):
                if i < len(solutions):
                    test_with_sol.append({
                        "input": t["input"],
                        "output": solutions[i],
                    })
                else:
                    test_with_sol.append({"input": t["input"]})
            ch = content_hash({"task_id": task_id,
                               "train": task["train"],
                               "test": test_with_sol})
            rule = GROUNDED_RULES.get(ch)
            if rule is None:
                n_missing_rule += 1
                continue
            _emit(out, {
                "task_id": task_id,
                "source": "training",
                "title": "",
                "difficulty": "",
                "skills": [],
                "written_solution": _STANDALONE_DESCRIPTIONS.get(ch, ""),
                "train": task["train"],
                "test": test_with_sol,
                "program_solution": rule,
                "solution_language": "racket",
                "needs_conversion": False,
            })
            n_training += 1

        # Section 2: augmented variants with solutions — share the
        # parent training task's rule (looked up by parent content_hash
        # via the training_hash_by_arc_id mapping built in section 1).
        for aug_path in sorted(AUG_DIR.glob("augmented_*.json")):
            task_id = aug_path.stem.replace("augmented_", "")
            # Augmented rows share rule with parent training row;
            # parent's content_hash is the rule key.
            parent_ch = _TRAINING_HASH_BY_TID.get(task_id)
            rule = GROUNDED_RULES.get(parent_ch) if parent_ch else None
            if rule is None:
                n_missing_rule += 1
                continue
            aug = load_json(aug_path)
            _emit(out, {
                "task_id": task_id,
                "source": "augmented",
                "title": "",
                "difficulty": "",
                "skills": [],
                "written_solution": _STANDALONE_DESCRIPTIONS.get(parent_ch, ""),
                "train": aug.get("train", []),
                "test": aug.get("test", []),
                "program_solution": rule,
                "solution_language": "racket",
                "needs_conversion": False,
            })
            n_augmented += 1

        # Section 3: custom hand-authored puzzles
        custom_hashed_path = CUSTOM_DIR / "all_tasks_hashed.json"
        name_to_hash_path = CUSTOM_DIR / "name_to_hash.json"
        n_custom = 0
        n_custom_rule_only = 0
        if custom_hashed_path.exists():
            custom = load_json(custom_hashed_path)
            name_map = (load_json(name_to_hash_path)
                        if name_to_hash_path.exists() else {})
            hash_to_name = {v: k for k, v in name_map.items()}
            for task_id, task in sorted(custom.items()):
                rule = task.get("rule") or ""
                if not rule:
                    n_missing_rule += 1
                    continue
                train = task.get("train") or []
                test = task.get("test") or []
                # Custom rules are authored as Racket; flag any that
                # don't start with `(rule!` so the conversion is visible.
                is_racket = rule.lstrip().startswith("(rule!")
                entry = {
                    "task_id": task_id,
                    "source": "custom",
                    "title": hash_to_name.get(task_id, ""),
                    "difficulty": task.get("difficulty", ""),
                    "skills": [],
                    "written_solution": task.get("pattern", ""),
                    "train": train,
                    "test": test,
                    "program_solution": rule if is_racket else "",
                    "solution_language": "racket",
                    "needs_conversion": not is_racket,
                }
                _emit(out, entry)
                n_custom += 1
                if not train and not test:
                    n_custom_rule_only += 1
                if not is_racket:
                    backlog_out.write(json.dumps({
                        "task_id": task_id,
                        "source": "custom",
                        "bank": None,
                        "original_id": task_id,
                        "title": hash_to_name.get(task_id, ""),
                        "written_solution": task.get("pattern", ""),
                        "function_name": "",
                        "python_source": rule,
                    }) + "\n")
                    n_backlogged += 1

        # Section 4: ALL puzzle banks under data/custom_puzzles/banks/<name>/
        # Each bank has a different schema; walk_banks handles the
        # variance via _bank_entry_to_canonical. Skipped-per-bank count
        # rolls up into n_missing_rule. needs_conversion entries also
        # write a parallel backlog row.
        n_custom_bank, n_bank_skipped, n_bank_backlogged = walk_banks(
            out, backlog_out)
        n_missing_rule += n_bank_skipped
        n_backlogged += n_bank_backlogged

        # Apply collision-resolved content_hash task_ids and flush.
        _finalize(out)

    # Summary + size
    size_bytes = OUT_PATH.stat().st_size
    print(f"wrote {OUT_PATH}")
    print(f"  training : {n_training}")
    print(f"  augmented: {n_augmented}")
    print(f"  custom   : {n_custom}  ({n_custom_rule_only} rule-only)")
    print(f"  banks    : {n_custom_bank}  across "
          f"{len(list(BANKS_DIR.iterdir())) if BANKS_DIR.exists() else 0} "
          f"banks/ subfolders")
    print(f"  total    : {n_training + n_augmented + n_custom + n_custom_bank} lines")
    print(f"  size     : {size_bytes/1e6:.1f} MB")
    if n_missing_rule:
        print(f"  skipped (no grounded/custom rule): {n_missing_rule}")
    if n_missing_solution:
        print(f"  skipped (no test solutions)      : {n_missing_solution}")
    if n_backlogged:
        print(f"wrote {BACKLOG_PATH}")
        print(f"  needs_conversion rows: {n_backlogged}")


if __name__ == "__main__":
    main()
