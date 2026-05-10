"""Regenerate manifest.json for every data/custom_puzzles/banks/<name>/.

Each manifest is auto-computed from that bank's puzzles.json (stats)
and a hand-written description (kept in this script, per bank name).
The linter checks that every bank has a manifest and that its counts
match the underlying puzzles.json.

Run:
    python3 scripts/regen_bank_manifests.py

This is idempotent — safe to run on every regen cycle.
"""
from __future__ import annotations
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANKS_DIR = ROOT / "data" / "custom_puzzles" / "banks"
sys.path.insert(0, str(ROOT / "scripts"))
from puzzle_ids import content_hash  # noqa: E402


# Per-bank hand-written metadata. The rest (counts, tags, schema shape)
# is derived from the puzzles.json file itself at build time.
BANK_DESCRIPTIONS: dict[str, dict] = {
    "v0_original": {
        "title": "Original 21-puzzle bank (v0)",
        "description": (
            "First iteration of the 21-puzzle bank. 7 easy + 7 medium + "
            "7 hard, each with 2-3 train pairs, 1 test pair, a written "
            "rule, and a Python reference solver (solutions.py). "
            "Task IDs: easy_01..hard_07."
        ),
        "schema_shape": "list[Entry]  (id/difficulty/name/tags/"
                        "written_rule/program_function/train/test)",
        "source": "user-provided download 2026-04-16",
        "solution_language": "python",
    },
    "v1_e_m_h_keys": {
        "title": "Bank with E/M/H-keyed dict",
        "description": (
            "Variant where the top-level is a dict keyed E1..H7. "
            "Each entry carries title + staged_hint + written_solution "
            "+ program_function. Useful for retrieval tasks that key "
            "on short IDs."
        ),
        "schema_shape": "dict[task_id → Entry]",
        "source": "user-provided download 2026-04-16",
        "solution_language": "python",
    },
    "v2_meta_puzzles": {
        "title": "Bank with meta/puzzles wrapper",
        "description": (
            "{meta, puzzles} wrapper — carries bank-level metadata "
            "alongside the entries. Entries include skills + scaffold "
            "+ reference_program (inline code)."
        ),
        "schema_shape": "{meta: {...}, puzzles: [Entry]}",
        "source": "user-provided download 2026-04-16",
        "solution_language": "python",
    },
    "v3_rich_schema": {
        "title": "Bank with richest per-task metadata",
        "description": (
            "The widest per-entry schema — id/title/difficulty/skills/"
            "written_solution/train/test/solver_name/scaffold/"
            "program_language/program_solution. Intended as the "
            "long-form reference with reasoning scaffolding."
        ),
        "schema_shape": "list[Entry]  (11 fields per entry)",
        "source": "user-provided download 2026-04-16",
        "solution_language": "python",
    },
    "additional_bank": {
        "title": "Additional 21-puzzle bank (E1-style IDs)",
        "description": (
            "Second hand-authored set of 21 puzzles with E1/M1/H1-style "
            "IDs. Biased toward marker-controlled transforms, bbox "
            "logic, and 2-pass patch-friendly tasks. Used together "
            "with the main bank for eval coverage."
        ),
        "schema_shape": "list[Entry]  (id/name/difficulty/tests/"
                        "written_solution/program_solution/train/test)",
        "source": "user-provided download 2026-04-16",
        "solution_language": "python",
    },
    "additional_scaffolded": {
        "title": "Additional bank with explicit scaffolding notes",
        "description": (
            "Scaffolded variant of the additional bank — each entry "
            "carries staged_hint + skills fields intended for staged/"
            "patch-friendly solvers. Test is split into test_input + "
            "test_output (not nested under `test`)."
        ),
        "schema_shape": "{metadata, puzzles: [Entry with test_input/"
                        "test_output]}",
        "source": "user-provided download 2026-04-16",
        "solution_language": "python",
    },
}


def _flatten_entries(raw) -> list[dict]:
    if isinstance(raw, list):
        return [e for e in raw if isinstance(e, dict)]
    if isinstance(raw, dict):
        if "puzzles" in raw:
            val = raw["puzzles"]
            if isinstance(val, dict):
                return [v for v in val.values() if isinstance(v, dict)]
            return [e for e in (val or []) if isinstance(e, dict)]
        return [v for v in raw.values() if isinstance(v, dict)]
    return []


def _compute_manifest(bank_dir: Path) -> dict:
    puzzles_path = bank_dir / "puzzles.json"
    sol_path = bank_dir / "solutions.py"
    ref_path = bank_dir / "REFERENCE.md"

    raw = json.loads(puzzles_path.read_text())
    entries = _flatten_entries(raw)

    difficulties: Counter = Counter()
    tag_totals: Counter = Counter()
    fields: Counter = Counter()
    n_train_pairs = 0
    n_test_pairs = 0
    for e in entries:
        if e.get("difficulty"):
            difficulties[str(e["difficulty"]).lower()] += 1
        for t in (e.get("tags") or e.get("skills") or []):
            tag_totals[str(t)] += 1
        for k in e:
            fields[k] += 1
        train = e.get("train") or []
        n_train_pairs += len(train)
        test = e.get("test")
        if test is None and e.get("test_input") is not None:
            test = [1]  # scalar count
        n_test_pairs += len(test) if test else 0

    meta = BANK_DESCRIPTIONS.get(bank_dir.name, {
        "title": bank_dir.name,
        "description": "(no description — add to BANK_DESCRIPTIONS "
                       "in scripts/regen_bank_manifests.py)",
        "schema_shape": "unknown",
        "source": "unknown",
        "solution_language": "unknown",
    })
    return {
        "bank": bank_dir.name,
        **meta,
        "files": {
            "puzzles_json": "puzzles.json"
                if puzzles_path.exists() else None,
            "solutions_py": "solutions.py"
                if sol_path.exists() else None,
            "reference_md": "REFERENCE.md"
                if ref_path.exists() else None,
        },
        "stats": {
            "n_puzzles": len(entries),
            "n_train_pairs": n_train_pairs,
            "n_test_pairs": n_test_pairs,
            "difficulties": dict(sorted(difficulties.items(),
                                        key=lambda kv: -kv[1])),
            "top_tags": [t for t, _ in tag_totals.most_common(10)],
            "common_fields": sorted(fields.keys()),
        },
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S %z")
            or time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def main():
    if not BANKS_DIR.is_dir():
        raise SystemExit(f"no banks dir at {BANKS_DIR}")
    for bank_dir in sorted(p for p in BANKS_DIR.iterdir() if p.is_dir()):
        if not (bank_dir / "puzzles.json").exists():
            continue
        manifest = _compute_manifest(bank_dir)
        out = bank_dir / "manifest.json"
        out.write_text(json.dumps(manifest, indent=2) + "\n")
        stats = manifest["stats"]
        print(f"  {bank_dir.name:<25} n={stats['n_puzzles']:>3}  "
              f"difficulties={stats['difficulties']}  "
              f"tags_seen={len(stats['top_tags'])}")


if __name__ == "__main__":
    main()
