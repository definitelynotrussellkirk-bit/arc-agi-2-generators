"""Compute the combinatorial reach of the generator corpus.

Each per-puzzle generator declares an AXES dict — the free parameters
of its input space. This script walks every generator, parses each
axis's `valid` field into a cardinality, and reports:

  - total reach across all generators (sum of per-generator products)
  - per-generator distribution
  - per-bank distribution
  - axes that don't fit the parser (so we know what's not counted)

This is the headline paper number: how many distinct task instances
the corpus can produce. Seed is treated as one extra axis so the
reach is reported BOTH excluding seed (configuration cardinality) and
including a bounded seed budget (for a runnable pass@k figure).

Run:
    python3 scripts/combinatorial_reach.py
    python3 scripts/combinatorial_reach.py --json out.json
    python3 scripts/combinatorial_reach.py --seed-budget 1000
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

PER = ROOT / "puzzle_generators" / "per_puzzle"

# Patterns the parser understands.
_INT_RANGE = re.compile(r"^\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*$")
_FLOAT_RANGE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*\.\.\s*(-?\d+(?:\.\d+)?)\s*$")
_PIPE_CHOICES = re.compile(r"^[^|]+(\|[^|]+)+$")


def _axis_cardinality(name: str, spec: dict) -> tuple[int | float, str]:
    """Return (cardinality, parser-tag) for one axis. cardinality is
    `math.inf` if we can't bound it (true freedom)."""
    valid = spec.get("valid")
    if valid is None:
        return math.inf, "no-valid-field"
    if isinstance(valid, list):
        return len(valid), "list"
    if not isinstance(valid, str):
        return math.inf, "non-string-valid"
    s = valid.strip()
    if s == "":
        return math.inf, "empty"
    # bool
    if s.lower() in {"true|false", "false|true"}:
        return 2, "bool"
    # pipe choices
    if "|" in s and _PIPE_CHOICES.match(s):
        choices = [c.strip() for c in s.split("|") if c.strip()]
        return len(choices), "choices"
    # int range
    m = _INT_RANGE.match(s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if b < a:
            return 1, "int-range-degenerate"
        return b - a + 1, "int-range"
    # float range — discretize to 100 buckets (heuristic — paper can
    # call this out explicitly)
    m = _FLOAT_RANGE.match(s)
    if m:
        return 100, "float-range-100-buckets"
    return math.inf, f"unparsed:{s[:30]}"


def _generator_reach(mod) -> tuple[int | float, dict]:
    """Per-generator reach = product over AXES cardinalities."""
    axes = getattr(mod, "AXES", {}) or {}
    if not axes:
        return 1, {}
    breakdown = {}
    total = 1
    has_inf = False
    for name, spec in axes.items():
        if not isinstance(spec, dict):
            breakdown[name] = ("?", "non-dict-spec")
            has_inf = True
            continue
        c, tag = _axis_cardinality(name, spec)
        breakdown[name] = (c, tag)
        if c == math.inf:
            has_inf = True
        else:
            total *= c
    if has_inf:
        # Don't multiply infinities into totals — the bounded reach is
        # what we report. Mark the generator as "has unbounded axes".
        return total, breakdown
    return total, breakdown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, help="Write per-generator records here")
    ap.add_argument("--seed-budget", type=int, default=1000,
                    help="Bounded seed count for the reach×seed report (default 1000)")
    ap.add_argument("--top-n", type=int, default=10,
                    help="Show this many highest-reach generators (default 10)")
    args = ap.parse_args()

    dirs = sorted(d for d in PER.iterdir()
                  if d.is_dir() and d.name not in ("__pycache__",)
                  and not d.name.startswith("__"))

    records = []
    parser_tag_counts: dict[str, int] = defaultdict(int)
    n_with_unbounded = 0
    for d in dirs:
        mod_name = f"puzzle_generators.per_puzzle.{d.name}.generator"
        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:
            records.append({"task_id": d.name, "error": str(e)[:200]})
            continue
        reach, breakdown = _generator_reach(mod)
        has_inf = any(c == math.inf for c, _ in breakdown.values())
        if has_inf:
            n_with_unbounded += 1
        for _, (_, tag) in breakdown.items():
            parser_tag_counts[tag] += 1
        records.append({
            "task_id": d.name,
            "reach": reach,
            "n_axes": len(breakdown),
            "has_unbounded_axis": has_inf,
            "axes": {k: {"cardinality": (c if c != math.inf else None),
                         "parse": tag}
                     for k, (c, tag) in breakdown.items()},
        })

    successful = [r for r in records if "error" not in r]
    total_reach = sum(r["reach"] for r in successful)
    nonzero = [r["reach"] for r in successful if r["reach"] > 1]
    nonzero.sort()
    median = nonzero[len(nonzero)//2] if nonzero else 0
    top = sorted(successful, key=lambda r: -r["reach"])[: args.top_n]

    # bounded-seed reach
    seed_budget = args.seed_budget
    total_with_seed = total_reach * seed_budget

    # Per-bank breakdown (read legacy_task_id from canonical to map back)
    bank_reach: dict[str, int] = defaultdict(int)
    bank_count: dict[str, int] = defaultdict(int)
    canonical = ROOT / "data" / "canonical" / "puzzle_db.jsonl"
    legacy_to_source = {}
    if canonical.exists():
        for line in canonical.read_text().splitlines():
            try:
                row = json.loads(line)
            except Exception:
                continue
            tid = row.get("task_id")
            src = row.get("source", "unknown")
            bank = row.get("bank") or src
            legacy_to_source[tid] = bank
    for r in successful:
        bank = legacy_to_source.get(r["task_id"], "unknown")
        bank_reach[bank] += r["reach"]
        bank_count[bank] += 1

    # Print summary
    print("="*70)
    print(f"Combinatorial reach — {len(successful)} generators")
    print("="*70)
    print(f"  total bounded configurations:  {total_reach:,}")
    print(f"      (≈ {total_reach:.2e})")
    print(f"  with seed budget {seed_budget}:    {total_with_seed:,}")
    print(f"      (≈ {total_with_seed:.2e})")
    print(f"  per-generator median:          {median:,}")
    print(f"  generators with unbounded axes: {n_with_unbounded}")
    print()
    print(f"Top {args.top_n} by reach:")
    for r in top:
        flag = "*" if r["has_unbounded_axis"] else " "
        print(f"  {flag} {r['task_id']:14s}  reach = {r['reach']:>12,}  axes = {r['n_axes']}")
    print()
    print("Per-bank totals:")
    for bank, total in sorted(bank_reach.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  {bank:55s}  n={bank_count[bank]:4d}  total={total:,}")
    print()
    print(f"Axis-parser tag distribution:")
    for tag, n in sorted(parser_tag_counts.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  {n:6d}  {tag}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        with args.json.open("w") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")
        print(f"\nWrote per-generator records to {args.json}")


if __name__ == "__main__":
    main()
