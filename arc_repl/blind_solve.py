"""
Blind solving workflow — ensures test answers are hidden until scoring.

Usage:
    s = BlindSession.random()
    s.explore()
    s.step('(feature! "diff" (diff @1 @2))')
    s.step('(rule! (lambda (g) (recolor g 8 7)))')
    s.test_all()
    s.submit(0)
    s.score()
"""

import sys
import random
import numpy as np
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.data_loader import load_challenges, load_solutions
from arc_repl.executor import ArcExecutor
from arc_repl.builtins import Grid, _unwrap


class BlindSession:
    """Blind solve session — test answers hidden until scoring."""

    def __init__(self, task_id, task, solution=None, auto_scan=False):
        self.task_id = task_id
        self.task = task
        self._solution = solution
        self._submissions = {}
        self._scored = False

        self.ex = ArcExecutor(task, auto_scan_on_load=auto_scan)

        # Track artifact refs for each pair and test
        self._pair_map = {}
        self._test_map = {}
        n = 0
        for i in range(len(task["train"])):
            n += 1
            in_ref = f"@{n}"
            n += 1
            out_ref = f"@{n}"
            self._pair_map[i] = (in_ref, out_ref)
        for i in range(len(task["test"])):
            n += 1
            self._test_map[i] = f"@{n}"

    @classmethod
    def random(cls, dataset="training", same_shape_only=True, seed=None, auto_scan=False):
        challenges = load_challenges(dataset)
        try:
            solutions = load_solutions(dataset)
        except FileNotFoundError:
            solutions = {}

        candidates = list(challenges.keys())
        if same_shape_only:
            candidates = [tid for tid in candidates if all(
                np.array(p["input"]).shape == np.array(p["output"]).shape
                for p in challenges[tid]["train"]
            )]

        if seed is not None:
            random.seed(seed)
        task_id = random.choice(candidates)
        return cls(task_id, challenges[task_id], solutions.get(task_id), auto_scan)

    @classmethod
    def pick(cls, task_id, dataset="training", auto_scan=False):
        challenges = load_challenges(dataset)
        try:
            solutions = load_solutions(dataset)
        except FileNotFoundError:
            solutions = {}
        return cls(task_id, challenges[task_id], solutions.get(task_id), auto_scan)

    def explore(self):
        """Print task overview."""
        t = self.task
        print(f"=== Task: {self.task_id} ===")
        print(f"Train pairs: {len(t['train'])}  |  Test inputs: {len(t['test'])}")
        for i, pair in enumerate(t["train"]):
            inp = np.array(pair["input"])
            out = np.array(pair["output"])
            in_ref, out_ref = self._pair_map[i]
            print(f"  Pair {i}: {in_ref}={list(inp.shape)} \u2192 {out_ref}={list(out.shape)}"
                  f"  in={sorted(set(inp.flatten().tolist()))}"
                  f"  out={sorted(set(out.flatten().tolist()))}")
        for i in range(len(t["test"])):
            inp = np.array(t["test"][i]["input"])
            ref = self._test_map[i]
            print(f"  Test {i}: {ref}={list(inp.shape)}"
                  f"  colors={sorted(set(inp.flatten().tolist()))}")
        print()

    def step(self, command):
        """Execute an S-expression command."""
        result = self.ex.step(command)
        print(result)
        return result

    def test_all(self):
        """Test current rule on ALL train pairs."""
        all_pass = True
        for i in range(len(self.task["train"])):
            result = self.ex.step(f"(test! {i})")
            print(result)
            if "FAIL" in result:
                all_pass = False
        if all_pass:
            print(f"\n ALL {len(self.task['train'])} PAIRS PASS")
        else:
            print(f"\n SOME PAIRS FAILED")
        return all_pass

    def show_grid(self, ref):
        """Display a grid."""
        print(self.ex.step(f"(show! {ref})"))

    def show_pair(self, pair_index):
        """Show a train pair."""
        in_ref, out_ref = self._pair_map[pair_index]
        print(f"--- Pair {pair_index} ---")
        print("Input:")
        self.show_grid(in_ref)
        print("Output:")
        self.show_grid(out_ref)

    def submit(self, test_index=0):
        """Apply rule to test input and store for scoring."""
        result = self.ex.step(f"(apply! {test_index})")
        print(result)

        last_ref = f"_{self.ex._result_n}"
        grid = self.ex._results.get(last_ref)
        if grid is None:
            print("ERROR: no result")
            return None

        self._submissions[test_index] = _unwrap(grid)
        remaining = len(self.task["test"]) - len(self._submissions)
        if remaining > 0:
            print(f"Stored test {test_index}. {remaining} remaining.")
        else:
            print(f"All {len(self._submissions)} test(s) stored. Call .score()")
        return _unwrap(grid)

    def score(self):
        """Reveal answers and check."""
        if not self._submissions:
            print("Nothing submitted.")
            return {}
        if self._solution is None:
            print("No solution available.")
            return {}

        results = {}
        all_correct = True
        for idx in sorted(self._submissions):
            got = self._submissions[idx]
            if idx >= len(self._solution):
                print(f"Test {idx}: no solution available")
                continue
            expected = self._solution[idx]
            match = got == expected
            if match:
                print(f"Test {idx}: CORRECT")
            else:
                ga, ea = np.array(got), np.array(expected)
                if ga.shape != ea.shape:
                    print(f"Test {idx}: WRONG \u2014 shape {list(ga.shape)} vs {list(ea.shape)}")
                else:
                    n = int((ga != ea).sum())
                    print(f"Test {idx}: WRONG \u2014 {n}/{ga.size} cells differ")
                    for r, c in list(zip(*np.where(ga != ea)))[:5]:
                        print(f"    ({r},{c}): got {ga[r,c]}, expected {ea[r,c]}")
                all_correct = False
            results[idx] = match

        if all_correct:
            print(f"\nALL {len(results)} TEST(S) CORRECT")
        self._scored = True
        return results
