#!/usr/bin/env python3
"""
Concept inventory — cluster every Racket-available puzzle by its
canonicalized rule and write the result to data/derived/concepts.jsonl.

Phase 1 of docs/PUZZLE_GENERATOR_ROADMAP.md. The output answers:

  - How many distinct concepts do we have?
  - Which concepts are heavily over-represented?
  - Which concepts are singletons (the long tail)?
  - Given a concept, which puzzles implement it?

Usage:
    python3 scripts/concept_inventory.py
    python3 scripts/concept_inventory.py --top 30      # show top concepts at end
    python3 scripts/concept_inventory.py --no-write    # dry run, no file write
    python3 scripts/concept_inventory.py --task ID     # one puzzle's hash only

Output JSONL (one row per concept_hash):
    {
      "concept_hash":      "<sha256[:12]>",
      "n_puzzles":         int,
      "member_task_ids":   [...],
      "member_files":      [...],   # paths under data/base/solutions
      "sample_template":   "<canonical rule with $cN slots>",
      "color_slot_count":  int,
      "size_slot_count":   int,
      "first_seen":        "<task_id of first member>",
      "n_augmented":       int,     # how many members live under augmented/
      "n_training":        int,     # how many under training/
      "n_bank":            int,     # under banks/
      "n_custom":          int      # under custom/
    }

Plus a sidecar `data/derived/concepts_uncanonicalizable.jsonl` listing
puzzles whose rules failed to canonicalize, with the reason.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.canonicalize_rule import canonicalize_rule  # noqa: E402

SOLUTIONS_DIR = ROOT / "data" / "base" / "solutions"
OUTPUT = ROOT / "data" / "derived" / "concepts.jsonl"
SIDECAR = ROOT / "data" / "derived" / "concepts_uncanonicalizable.jsonl"


def _source_bucket(rel_path: str) -> str:
    """Coarse-bucket a solution file by its location under data/base/solutions."""
    if "/augmented/" in rel_path: return "augmented"
    if "/training/" in rel_path:  return "training"
    if "/banks/" in rel_path:     return "bank"
    if "/custom/" in rel_path:    return "custom"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top", type=int, default=15,
                    help="Number of top concepts to display in stdout summary")
    ap.add_argument("--no-write", action="store_true",
                    help="Don't write output files; print summary only")
    ap.add_argument("--task", help="Show concept hash for a single task_id and exit")
    args = ap.parse_args()

    if args.task:
        return _show_one(args.task)

    if not SOLUTIONS_DIR.exists():
        print(f"missing: {SOLUTIONS_DIR}", file=sys.stderr); sys.exit(1)

    t0 = time.time()
    by_concept: dict[str, dict] = {}
    uncanonicalizable: list[dict] = []
    skipped_no_racket = 0
    skipped_needs_conversion = 0
    inspected = 0

    for path in sorted(SOLUTIONS_DIR.rglob("*.json")):
        try:
            d = json.loads(path.read_text())
        except Exception:
            continue
        rt = d.get("racket_target") or {}
        # Skip puzzles still flagged for conversion — codex hasn't filled them in.
        if rt.get("needs_conversion"):
            skipped_needs_conversion += 1
            continue
        src = (rt.get("target_code") or rt.get("raw_code") or "").strip()
        if not src:
            skipped_no_racket += 1
            continue

        inspected += 1
        info = canonicalize_rule(src)
        if info["concept_hash"] is None:
            uncanonicalizable.append({
                "task_id": d.get("task_id"),
                "file": str(path.relative_to(ROOT)),
                "reason": info.get("reason", "unknown"),
            })
            continue

        h = info["concept_hash"]
        rel = str(path.relative_to(ROOT))
        bucket = _source_bucket(rel)
        if h not in by_concept:
            by_concept[h] = {
                "concept_hash":      h,
                "n_puzzles":         0,
                "member_task_ids":   [],
                "member_files":      [],
                "sample_template":   info["template"],
                "color_slot_count":  len(info["color_slots"]),
                "size_slot_count":   len(info["size_slots"]),
                "first_seen":        d.get("task_id"),
                "n_augmented":       0,
                "n_training":        0,
                "n_bank":            0,
                "n_custom":          0,
            }
        rec = by_concept[h]
        rec["n_puzzles"] += 1
        rec["member_task_ids"].append(d.get("task_id"))
        rec["member_files"].append(rel)
        if bucket == "augmented": rec["n_augmented"] += 1
        elif bucket == "training": rec["n_training"] += 1
        elif bucket == "bank":     rec["n_bank"] += 1
        elif bucket == "custom":   rec["n_custom"] += 1

    elapsed = time.time() - t0

    # Sort concepts by cardinality desc for deterministic output.
    rows = sorted(by_concept.values(), key=lambda r: (-r["n_puzzles"], r["concept_hash"]))

    if not args.no_write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT.open("w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        with SIDECAR.open("w") as f:
            for u in uncanonicalizable:
                f.write(json.dumps(u, ensure_ascii=False) + "\n")
        out_msg = f"wrote {OUTPUT.relative_to(ROOT)} ({len(rows)} concepts)"
        sidecar_msg = f"wrote {SIDECAR.relative_to(ROOT)} ({len(uncanonicalizable)} uncanonicalizable)"
    else:
        out_msg = f"(dry-run) would write {len(rows)} concepts"
        sidecar_msg = f"(dry-run) {len(uncanonicalizable)} uncanonicalizable"

    # Summary
    print(f"inspected:                {inspected:>5}")
    print(f"  skipped (no racket):    {skipped_no_racket:>5}")
    print(f"  skipped (needs_convert):{skipped_needs_conversion:>5}")
    print(f"  uncanonicalizable:      {len(uncanonicalizable):>5}")
    print(f"distinct concepts:        {len(rows):>5}")
    if rows:
        singletons = sum(1 for r in rows if r["n_puzzles"] == 1)
        big = sum(1 for r in rows if r["n_puzzles"] >= 10)
        print(f"  singletons:             {singletons:>5}")
        print(f"  >=10 members:           {big:>5}")
        print(f"  largest cluster:        {rows[0]['n_puzzles']} puzzles "
              f"({rows[0]['concept_hash']}, slots={rows[0]['color_slot_count']})")

    if args.top and rows:
        print()
        print(f"Top {min(args.top, len(rows))} concepts by cardinality:")
        print(f"  {'hash':<14} {'n':>4} {'slots':>5} {'aug':>4} {'tr':>4} {'bnk':>4} {'cust':>4}  first_member")
        for r in rows[: args.top]:
            print(f"  {r['concept_hash']:<14} {r['n_puzzles']:>4} "
                  f"{r['color_slot_count']:>5} {r['n_augmented']:>4} "
                  f"{r['n_training']:>4} {r['n_bank']:>4} {r['n_custom']:>4}  {r['first_seen']}")

    print()
    print(out_msg)
    print(sidecar_msg)
    print(f"elapsed: {elapsed:.1f}s")


def _show_one(task_id: str) -> None:
    """Helper: print the concept hash for one puzzle."""
    import glob
    for f in glob.glob(str(SOLUTIONS_DIR / "**/*.json"), recursive=True):
        d = json.loads(Path(f).read_text())
        if d.get("task_id") != task_id:
            continue
        rt = d.get("racket_target") or {}
        src = rt.get("target_code") or rt.get("raw_code") or ""
        if not src.strip():
            print(f"{task_id}: no racket source"); return
        info = canonicalize_rule(src)
        print(f"task_id:      {task_id}")
        print(f"concept_hash: {info['concept_hash']}")
        print(f"color_slots:  {info['color_slots']}")
        print(f"file:         {Path(f).relative_to(ROOT)}")
        return
    print(f"task_id {task_id} not found", file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
