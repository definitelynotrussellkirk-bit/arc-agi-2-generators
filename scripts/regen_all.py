"""Single-command regen of the puzzle pipeline.

Runs, in order:
  1. scripts/build_canonical_puzzles.py   — puzzles.jsonl
  2. scripts/build_puzzle_db.py           — puzzle_db.jsonl (metadata DB)
  3. scripts/regen_bank_manifests.py      — per-bank manifest.json
  4. scripts/puzzle_docs.py regen         — docs/PUZZLE_BANK.md
  5. scripts/concept_inventory.py         — data/derived/concepts.jsonl  (cheap, ~3s)
  6. scripts/lint_puzzles.py              — final validation gate

If any step fails, prints the tail + exits non-zero. On full pass
prints a one-line summary.

Run:
    python3 scripts/regen_all.py                    # full cycle
    python3 scripts/regen_all.py --no-lint          # skip the gate (dev)
    python3 scripts/regen_all.py --skip-concepts    # skip concept inventory
    python3 scripts/regen_all.py --with-behavioral  # also run behavioral hash (~2 min)
"""
from __future__ import annotations
import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("canonical",  ["scripts/build_canonical_puzzles.py"]),
    ("db",         ["scripts/build_puzzle_db.py"]),
    ("manifests",  ["scripts/regen_bank_manifests.py"]),
    ("doc",        ["scripts/puzzle_docs.py", "regen", "--no-canonical"]),
    ("gen_lint",   ["scripts/lint_generators.py",
                    "--json", "data/derived/generator_lint.jsonl",
                    "--fail-on", "errors"]),
]

# Phase 1 of the generator roadmap — cheap concept inventory + lint integration.
CONCEPT_STEP = ("concepts", ["scripts/concept_inventory.py"])

# Phase 7 — behavioral hash + concept merge proposals. Slower (~2 min);
# off by default. Enable with --with-behavioral.
BEHAVIORAL_STEPS = [
    ("behavioral_hash", ["scripts/behavioral_hash.py"]),
    ("concept_merge",   ["scripts/concept_merge.py", "--apply"]),
]


def run_step(name: str, argv: list[str]) -> bool:
    cmd = [sys.executable, *[str(ROOT / argv[0])], *argv[1:]]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True,
                       text=True, timeout=600)  # 10 min for slow steps (behavioral_hash)
    dt = time.time() - t0
    if r.returncode == 0:
        last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        print(f"  ✓ {name:<10} {dt:5.1f}s   {last[:100]}")
        return True
    print(f"  ✗ {name:<10} {dt:5.1f}s   FAILED")
    print("  ── stdout tail ──")
    for line in r.stdout.strip().splitlines()[-10:]:
        print(f"    {line}")
    print("  ── stderr tail ──")
    for line in r.stderr.strip().splitlines()[-10:]:
        print(f"    {line}")
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-lint", action="store_true",
                    help="skip the final lint gate")
    ap.add_argument("--skip-concepts", action="store_true",
                    help="skip the concept_inventory step")
    ap.add_argument("--with-behavioral", action="store_true",
                    help="also run behavioral_hash + concept_merge (~2 min)")
    args = ap.parse_args()

    print(f"regen_all — {time.strftime('%Y-%m-%d %H:%M:%S')}")
    t0 = time.time()
    steps_to_run = list(STEPS)
    if not args.skip_concepts:
        steps_to_run.append(CONCEPT_STEP)
    if args.with_behavioral:
        steps_to_run.extend(BEHAVIORAL_STEPS)
    for name, argv in steps_to_run:
        if not run_step(name, argv):
            print(f"\n✗ aborted at step '{name}'")
            sys.exit(1)
    if not args.no_lint:
        ok = run_step("lint", ["scripts/lint_puzzles.py"])
        if not ok:
            print(f"\n✗ lint gate failed")
            sys.exit(1)
    print(f"\n✓ all steps passed in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
