"""Walkthrough of the ARC REPL — diagnose, diff, try, test, auto-scan, render.

Run: python3 examples/repl_demo.py

The REPL takes a task dict ({"train": [...], "test": [...]}), exposes
S-expression macros for exploring/transforming/verifying, and tracks
artifacts (@N grids, _N results, !N pass/fail checks, &N rules).

Each section below uses one tiny task so the output stays readable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from arc_repl.executor import ArcExecutor


def banner(title):
    print(f"\n=== {title} " + "=" * (60 - len(title)))


# ---------------------------------------------------------------------------
# Task 1 — vertical flip. The rule is `(flip-ud g)`.
# ---------------------------------------------------------------------------
flip_task = {
    "train": [
        {"input": [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
         "output": [[0, 0, 3], [0, 2, 0], [1, 0, 0]]},
        {"input": [[5, 5, 0], [0, 0, 0], [0, 0, 7]],
         "output": [[0, 0, 7], [0, 0, 0], [5, 5, 0]]},
    ],
    "test": [{"input": [[8, 0, 0], [0, 9, 0], [0, 0, 4]]}],
}

banner("1. diagnose! — shapes, color roles, per-pair diff summary")
x = ArcExecutor(flip_task, auto_scan_on_load=False)
print(x.step("(diagnose!)"))

banner("2. try! — test an idea WITHOUT committing to a rule")
print(x.step("(try! (lambda (g) (flip-ud g)) 0)"))
print(x.step("(try! (lambda (g) (flip-lr g)) 0)"))  # wrong on purpose

banner("3. rule! + test-all! — commit and verify")
print(x.step("(rule! (flip-ud g))"))
print(x.step("(test-all!)"))

banner("4. apply! + submit! — produce test attempts")
print(x.step("(apply! 0)"))
print(x.step("(submit! _1)"))


# ---------------------------------------------------------------------------
# Task 2 — recolor 1→7, 2→3.  Demonstrate auto-scan and suggest.
# ---------------------------------------------------------------------------
recolor_task = {
    "train": [
        {"input": [[1, 1, 2], [0, 2, 1], [2, 0, 1]],
         "output": [[7, 7, 3], [0, 3, 7], [3, 0, 7]]},
        {"input": [[2, 0, 1], [1, 2, 0], [0, 1, 2]],
         "output": [[3, 0, 7], [7, 3, 0], [0, 7, 3]]},
    ],
    "test": [{"input": [[1, 2, 0], [0, 1, 2], [2, 1, 0]]}],
}

banner("5. auto-scan! — runs every feature, ranks by informativeness")
x = ArcExecutor(recolor_task, auto_scan_on_load=False)
# Auto-scan output can be long; show the top entries.
scan_out = x.step("(auto-scan!)").splitlines()
print("\n".join(scan_out[:15]))
if len(scan_out) > 15:
    print(f"... ({len(scan_out) - 15} more lines)")

banner("6. suggest! — map scan profile to candidate rules")
print(x.step("(suggest!)"))


# ---------------------------------------------------------------------------
# Task 3 — show the LAYERED FAILURE DIFF when a rule is almost-right.
# Rule should recolor 1→7. We set it to 1→8 on purpose to see the diff.
# ---------------------------------------------------------------------------
banner("7. layered diff on a wrong rule — bbox, per-color +/-, recolors")
recolor_simple = {
    "train": [
        {"input": [[1, 0, 1], [0, 1, 0]],
         "output": [[7, 0, 7], [0, 7, 0]]},
    ],
    "test": [{"input": [[1, 1, 0]]}],
}
x = ArcExecutor(recolor_simple, auto_scan_on_load=False)
print(x.step("(rule! (recolor g 1 8))"))  # WRONG: should be 1 → 7
print(x.step("(test! 0)"))
# Output shows:
#   - bbox of differing cells
#   - per-color delta:  color 7: +3 at (...)
#                       color 8: -3
#   - recolors: 8→7(3)
# That last line is the canonical "almost right" hint.

# Now fix it and confirm.
print()
print(x.step("(rule! (recolor g 1 7))"))
print(x.step("(test! 0)"))


# ---------------------------------------------------------------------------
# Task 4 — render! writes PNGs to /tmp.  Pure side-effect demo.
# ---------------------------------------------------------------------------
banner("8. render! — PNGs to /tmp for visual inspection")
x = ArcExecutor(flip_task, auto_scan_on_load=False)
print(x.step("(render! task)"))
print(x.step("(render! pair 0)"))
x.step("(rule! (flip-ud g))")
print(x.step("(render! diff 0)"))  # rule output vs expected
print("\nOpen the PNGs above to see the task/pair/rule-diff visualization.")
