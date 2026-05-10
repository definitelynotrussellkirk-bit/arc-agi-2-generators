"""Build data/canonical/puzzle_db.jsonl — a lightweight per-puzzle DB.

One line per puzzle, keyed by task_id. Unlike puzzles.jsonl (which
carries the full train/test grids + solution code), this DB is a
metadata-only projection sized for browsing, filtering, ELO tracking,
and report generation. It's the table-of-contents for puzzles.jsonl.

Each DB row:

    {
      "task_id":          "v0_original:easy_01"   # unique primary key
      "source":           "bank:v0_original"      # broad category
      "bank":             "v0_original"           # None for non-bank sources
      "original_id":      "easy_01"               # pre-prefix id
      "title":            "Fill hollow-square centers"   # canonical name
      "written_solution": "Whenever a 3x3 ring …" # prose description
      "difficulty":       "easy" | "medium" | "hard" | ""
      "skills":           ["same_size_local", ...] # canonical (was "tags")
      "n_train":          2
      "n_test":           1
      "input_dims":       [3, 3]
      "output_dims":      [3, 3]
      "palette_size":     3
      "size_relation":    "same_size" | "output_smaller" | …
      "solution_language":"racket"                 # always "racket" post-cleanup
      "needs_conversion": bool                     # true while Racket text empty
      "racket_primitives":[...]                    # mined from program_solution
      "elo":              null                     # TBD
      "elo_updated_at":   null
      "created_at":       "2026-04-16 …"
    }

Run:
    python3 scripts/build_puzzle_db.py

Safe to re-run (preserves ELO + created_at from existing DB).
"""
from __future__ import annotations
import json
import time
from pathlib import Path

import sys
ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "data" / "canonical" / "puzzles.jsonl"
DB_PATH = ROOT / "data" / "canonical" / "puzzle_db.jsonl"
sys.path.insert(0, str(ROOT / "scripts"))
from puzzle_ids import (
    compute_puzzle_ids, extract_racket_primitives,
)


def _load_existing_db() -> dict[str, dict]:
    if not DB_PATH.exists():
        return {}
    out = {}
    for line in DB_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
            out[r["task_id"]] = r
        except Exception:
            continue
    return out


def _summary_fields(entry: dict) -> dict:
    """Derive lightweight metadata from a full canonical entry."""
    train = entry.get("train") or []
    test = entry.get("test") or []
    first = train[0] if train else (test[0] if test else {})
    inp = first.get("input")
    out = first.get("output")
    in_dims = [len(inp), len(inp[0])] if inp and inp[0] else [0, 0]
    out_dims = [len(out), len(out[0])] if out and out[0] else [0, 0]
    palette: set[int] = set()
    if inp:
        for row in inp:
            palette.update(row)
    if out:
        for row in out:
            palette.update(row)
    if in_dims == out_dims:
        size_relation = "same_size"
    elif in_dims[0] > out_dims[0] or in_dims[1] > out_dims[1]:
        size_relation = "output_smaller"
    elif in_dims[0] < out_dims[0] or in_dims[1] < out_dims[1]:
        size_relation = "output_larger"
    else:
        size_relation = "unknown"
    return {
        "n_train": len(train),
        "n_test": len(test),
        "input_dims": in_dims,
        "output_dims": out_dims,
        "palette_size": len(palette),
        "size_relation": size_relation,
    }


def _source_category(entry: dict) -> tuple[str, str | None]:
    """Return (coarse_source, bank_name)."""
    src = entry.get("source", "")
    if src.startswith("bank:"):
        return "bank", src.split(":", 1)[1]
    return src, None


def main():
    if not CANONICAL.exists():
        raise SystemExit(
            f"{CANONICAL} missing — run scripts/build_canonical_puzzles.py first"
        )

    existing = _load_existing_db()
    now = time.strftime("%Y-%m-%d %H:%M:%S %z") or \
          time.strftime("%Y-%m-%d %H:%M:%S")

    rows: list[dict] = []
    with CANONICAL.open() as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            e = json.loads(raw)
            tid = e["task_id"]
            source, bank = _source_category(e)

            stats = _summary_fields(e)

            difficulty = str(e.get("difficulty", "")).lower()
            skills = e.get("skills") or []
            written = e.get("written_solution") or ""
            solution_language = e.get("solution_language") or "racket"
            needs_conversion = bool(e.get("needs_conversion"))

            # Prefer the canonical-stamped hash/slug; recompute as
            # fallback to keep the DB self-healing if canonical lacks them.
            ch = e.get("content_hash") or compute_puzzle_ids(e)[0]
            slug = e.get("slug") or compute_puzzle_ids(e)[1]
            parent_hash = e.get("parent_hash")
            parent_reason = e.get("parent_reason")

            # Primitives used in the Racket solution — tagging signal.
            racket_prims = extract_racket_primitives(
                e.get("program_solution") or "")

            prev = existing.get(tid, {})
            row = {
                "task_id": tid,
                "legacy_task_id": e.get("legacy_task_id"),
                "content_hash": ch,
                "slug": slug,
                "source": e.get("source", ""),
                "bank": bank,
                "original_id": e.get("original_id", tid),
                "parent_hash": parent_hash,
                "parent_reason": parent_reason,
                "title": e.get("title", ""),
                "written_solution": written,
                "difficulty": difficulty,
                "skills": skills,
                **stats,
                "solution_language": solution_language,
                "needs_conversion": needs_conversion,
                "racket_primitives": racket_prims,
                # ELO — preserved across rebuilds; None on first emit
                "elo": prev.get("elo"),
                "elo_updated_at": prev.get("elo_updated_at"),
                "created_at": prev.get("created_at", now),
                "last_seen_at": now,
            }
            rows.append(row)

    DB_PATH.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n"
    )
    print(f"wrote {DB_PATH}  ({len(rows)} rows, "
          f"{DB_PATH.stat().st_size/1e6:.1f} MB)")
    # Summary
    from collections import Counter
    by_source = Counter(r["source"] for r in rows)
    by_diff = Counter(r["difficulty"] for r in rows if r["difficulty"])
    print(f"  by source   : {dict(by_source)}")
    print(f"  by difficulty: {dict(by_diff)}")
    n_with_elo = sum(1 for r in rows if r["elo"] is not None)
    n_with_parent = sum(1 for r in rows if r.get("parent_hash"))
    n_with_racket_prims = sum(1 for r in rows if r["racket_primitives"])
    n_needs_conversion = sum(1 for r in rows if r.get("needs_conversion"))
    print(f"  with ELO         : {n_with_elo}/{len(rows)} (others TBD)")
    print(f"  with parent      : {n_with_parent}/{len(rows)} "
          "(augmented→training links)")
    print(f"  racket prims     : {n_with_racket_prims}/{len(rows)}")
    print(f"  needs_conversion : {n_needs_conversion}/{len(rows)} "
          "(work-list in data/derived/conversion_backlog.jsonl)")

    # Dedup signal: unique content hashes.
    from collections import Counter
    hash_counts = Counter(r["content_hash"] for r in rows)
    collisions = [h for h, n in hash_counts.items() if n > 1]
    if collisions:
        print(f"  content hash collisions: {len(collisions)} "
              f"(e.g., {collisions[:2]})")


if __name__ == "__main__":
    main()
