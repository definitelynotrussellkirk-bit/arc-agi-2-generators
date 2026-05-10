#!/usr/bin/env python3
"""Run every project lint and report a unified summary.

Wraps the existing lint scripts and produces a single status table.
Doesn't replace any of them — they remain runnable individually.

Lints invoked:
  1. scripts/build_arc_reference.py --validate    (DB integrity)
  2. scripts/lint_descriptions.py                 (lexical vocab + structure)
  3. scripts/lint_description_rule_consistency.py (cross-artifact)
  4. scripts/lint_puzzles.py                      (existing 7-check suite)

Optional / slow:
  5. scripts/lint_generators.py                   (puzzle generator validation)
     Skipped by default (~5+ min). Pass --with-generators to include.

Exit code:
  0 = every lint exits 0 OR is a known-noisy heuristic
  1 = at least one lint reports a hard failure
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], timeout: int = 300) -> tuple[int, str, float]:
    t0 = time.time()
    try:
        r = subprocess.run(
            [sys.executable] + cmd, cwd=str(ROOT),
            capture_output=True, text=True, timeout=timeout,
        )
        return r.returncode, (r.stdout + r.stderr), time.time() - t0
    except subprocess.TimeoutExpired:
        return -1, f"<timeout after {timeout}s>", time.time() - t0


def parse_lint_descriptions_summary(out: str) -> dict:
    """Pull rows-scanned + clean-rate out of lint_descriptions.py output."""
    info = {}
    m = re.search(r"rows scanned:\s+(\d+)", out)
    if m: info["rows"] = int(m.group(1))
    m = re.search(r"clean \(0 findings\):\s+(\d+)", out)
    if m: info["clean"] = int(m.group(1))
    m = re.search(r"findings by severity:\s+(\{[^}]*\})", out)
    if m:
        try:
            import ast
            info["severities"] = ast.literal_eval(m.group(1))
        except Exception:
            pass
    return info


def parse_consistency_summary(out: str) -> dict:
    info = {}
    m = re.search(r"pairs scanned:\s+(\d+)", out)
    if m: info["pairs"] = int(m.group(1))
    m = re.search(r"clean:\s+(\d+)", out)
    if m: info["clean"] = int(m.group(1))
    m = re.search(r"flagged:\s+(\d+)", out)
    if m: info["flagged"] = int(m.group(1))
    return info


def parse_lint_puzzles_summary(out: str) -> dict:
    info = {}
    m = re.search(r"(\d+)/(\d+) checks failed", out)
    if m:
        info["failed"] = int(m.group(1))
        info["total"] = int(m.group(2))
        return info
    m = re.search(r"(\d+)/(\d+) checks passed", out)
    if m:
        info["failed"] = 0
        info["total"] = int(m.group(2))
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-generators", action="store_true",
                    help="include scripts/lint_generators.py (~5+ min)")
    args = ap.parse_args()

    print("=" * 70)
    print("ARC-AGI-2 lint suite")
    print("=" * 70)

    results = []

    # 1. DB validate
    rc, out, el = run(["scripts/build_arc_reference.py", "--validate"])
    ok = rc == 0
    print(f"\n[1] arc_reference.jsonl validate    {'OK' if ok else 'FAIL':6}  ({el:.1f}s)")
    if not ok:
        for line in out.splitlines()[-15:]:
            print(f"    {line}")
    results.append(("db_validate", ok, el))

    # 2. lexical descriptions
    rc, out, el = run(["scripts/lint_descriptions.py"])
    info = parse_lint_descriptions_summary(out)
    rate = info.get("clean", 0) / max(info.get("rows", 1), 1)
    severities = info.get("severities", {})
    n_errors = severities.get("error", 0)
    print(f"[2] lexical descriptions             "
          f"{info.get('clean', '?')}/{info.get('rows', '?')} clean "
          f"({rate:.1%})  severities={severities}  ({el:.1f}s)")
    # SUPER STRICT — any error-severity finding fails the suite.
    results.append(("lexical_descriptions", n_errors == 0 and rate >= 0.95, el))

    # 3. cross-consistency
    rc, out, el = run(["scripts/lint_description_rule_consistency.py"])
    info = parse_consistency_summary(out)
    rate = info.get("clean", 0) / max(info.get("pairs", 1), 1)
    print(f"[3] description ↔ rule consistency   "
          f"{info.get('clean', '?')}/{info.get('pairs', '?')} clean "
          f"({rate:.1%})  flagged={info.get('flagged', '?')}  ({el:.1f}s)")
    results.append(("consistency", rate >= 0.90, el))

    # 3b. description coverage (informational — does not gate)
    rc, out, el = run(["scripts/lint_description_coverage.py"])
    m = re.search(r"WITHOUT description:\s+(\d+)\s+\(([\d.]+)%\)", out)
    if m:
        print(f"[3b] description coverage           "
              f"{m.group(1)} missing ({m.group(2)}%)  ({el:.1f}s)")
    else:
        print(f"[3b] description coverage           ?  ({el:.1f}s)")
    results.append(("description_coverage", True, el))  # info-only, never blocks

    # 3c. Racket style (informational for warns; broken-binding is hard fail)
    rc, out, el = run(["scripts/lint_racket_style.py"])
    m_or = re.search(r"for-or-value-search\s+(\d+)", out)
    m_first = re.search(r"for-first-value-search\s+(\d+)", out)
    m_size = re.search(r"oversized-rule\s+(\d+)", out)
    m_broken = re.search(r"for-comprehension-broken-binding\s+(\d+)", out)
    counts = []
    if m_or: counts.append(f"for/or={m_or.group(1)}")
    if m_first: counts.append(f"for/first={m_first.group(1)}")
    if m_size: counts.append(f"oversized={m_size.group(1)}")
    if m_broken: counts.append(f"BROKEN-BIND={m_broken.group(1)}")
    print(f"[3c] Racket-rule style              "
          f"{', '.join(counts) if counts else '?'}  ({el:.1f}s)")
    # Broken bindings are real parse errors — gate on them.
    n_broken = int(m_broken.group(1)) if m_broken else 0
    results.append(("racket_style", n_broken == 0, el))

    # 4. lint_puzzles (slow ~30s)
    rc, out, el = run(["scripts/lint_puzzles.py"], timeout=120)
    info = parse_lint_puzzles_summary(out)
    if info.get("failed") is not None:
        ok = info["failed"] == 0
        print(f"[4] puzzle lint suite                "
              f"{'OK' if ok else 'FAIL':6}  "
              f"{info.get('failed', '?')}/{info.get('total', '?')} checks failed  ({el:.1f}s)")
        if not ok:
            for line in out.splitlines():
                if 'FAIL' in line: print(f"    {line.strip()}")
        results.append(("lint_puzzles", ok, el))
    else:
        print(f"[4] puzzle lint suite                ?  ({el:.1f}s)")
        results.append(("lint_puzzles", False, el))

    # 5. generator lint (optional)
    if args.with_generators:
        rc, out, el = run(["scripts/lint_generators.py"], timeout=900)
        ok = rc == 0
        print(f"[5] generator lint                   "
              f"{'OK' if ok else 'FAIL':6}  ({el:.1f}s)")
        results.append(("lint_generators", ok, el))

    print()
    print("=" * 70)
    n_ok = sum(1 for _, ok, _ in results if ok)
    n_total = len(results)
    print(f"OVERALL  {n_ok}/{n_total} OK")
    if n_ok != n_total:
        print(f"FAILED:")
        for name, ok, _ in results:
            if not ok:
                print(f"  - {name}")
    sys.exit(0 if n_ok == n_total else 1)


if __name__ == "__main__":
    main()
