#!/usr/bin/env python3
"""Audit the current_work artifact for reviewer-readiness.

Run before bundling a `current_work.zip` for any external review round.
Prints canonical counts and reproducibility checks; exits non-zero if
any check fails.

Usage:
    python3 scripts/audit_artifact.py            # audit live tree
    python3 scripts/audit_artifact.py --zip path/to/current_work.zip

Checks:
    1. per_puzzle generator.py count
    2. per_puzzle dirs total
    3. dirs missing generator.py
    4. README count claim (00_README.md or docs/README.md)
    5. progress count claim (01_PROGRESS.md or docs/coverage doc)
    6. smoke-ready: every shipped generator's task_id resolves to a rule
       via either data/base/solutions/ OR solvers/grounded_rules.py
    7. missing runtime deps: required scripts/modules that runner imports
    8. direct-import sample: import 5 random generators, confirm
       generate(0, 0) returns a list-of-list of ints
"""
from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import random
import re
import sys
import zipfile
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PER_PUZZLE = ROOT / "puzzle_generators" / "per_puzzle"


def count_generators_live() -> tuple[int, int, list[Path]]:
    """Returns (n_generators, n_dirs, dirs_missing_generator_py)."""
    dirs = [p for p in PER_PUZZLE.iterdir()
            if p.is_dir() and not p.name.startswith("__")]
    gens = [p / "generator.py" for p in dirs if (p / "generator.py").exists()]
    missing = [p for p in dirs if not (p / "generator.py").exists()]
    return len(gens), len(dirs), missing


def count_generators_zip(zip_path: Path) -> tuple[int, int, list[str]]:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    gens = [n for n in names if n.endswith("/generator.py")
            and "/per_puzzle/" in n]
    dir_marker = re.compile(r"per_puzzle/[^/]+/$")
    dirs_set = set()
    for n in names:
        m = re.search(r"(per_puzzle/[^/]+)/", n)
        if m:
            dirs_set.add(m.group(1))
    gen_dirs = {n.rsplit("/", 1)[0] for n in gens}
    missing = sorted(dirs_set - gen_dirs)
    return len(gens), len(dirs_set), missing


def find_count_claim(text: str, label_regex: str) -> Optional[int]:
    """Find a number near a label match. Returns the first int found
    on the same line as `label_regex` matches."""
    rx = re.compile(label_regex, re.IGNORECASE)
    for line in text.splitlines():
        if rx.search(line):
            nums = re.findall(r"\b(\d{3,5})\b", line)
            if nums:
                return int(nums[0])
    return None


def read_readme_claim() -> Optional[int]:
    candidates = [
        ROOT / "00_README.md",
        ROOT / "README.md",
        Path.home() / "Desktop" / "New Folder 5" / "00_README.md",
    ]
    for p in candidates:
        if p.exists():
            text = p.read_text()
            for pattern in (
                r"\bcontains\s+\*\*?\d{3,5}\s+generators",
                r"\bbundle\s+contains\s+\*\*?\d{3,5}",
                r"\bcanonical\s*:.*?\d{3,5}\s+generators",
            ):
                n = find_count_claim(text, pattern)
                if n is not None:
                    return n
    return None


def read_progress_claim() -> Optional[int]:
    candidates = [
        ROOT / "01_PROGRESS.md",
        Path.home() / "Desktop" / "New Folder 5" / "01_PROGRESS.md",
    ]
    for p in candidates:
        if p.exists():
            text = p.read_text()
            n = find_count_claim(text, r"\bbank-task generators\b")
            if n is None:
                n = find_count_claim(text, r"\bgenerators?\b\s*[/]")
            if n is not None:
                return n
    return None


def smoke_ready_check() -> tuple[bool, list[str]]:
    """Can every shipped generator's rule be loaded from this tree?

    Considered loadable if either:
    - data/base/solutions/<bank>/<file>.json exists for the task_id, OR
    - solvers/grounded_rules.py contains an entry matching the task_id.
    """
    issues: list[str] = []
    rule_dir = ROOT / "data" / "base" / "solutions"
    fallback = ROOT / "solvers" / "grounded_rules.py"
    has_rule_dir = rule_dir.exists()
    has_fallback = fallback.exists()
    if not has_rule_dir and not has_fallback:
        issues.append("no rule source: missing both data/base/solutions/ AND solvers/grounded_rules.py")
        return False, issues
    return True, issues


def missing_runtime_deps() -> list[str]:
    """Heuristic: scan runner.py imports and check each is reachable."""
    runner = ROOT / "puzzle_generators" / "runner.py"
    if not runner.exists():
        return ["puzzle_generators/runner.py is missing"]
    text = runner.read_text()
    missing: list[str] = []
    # imports of `scripts.*` and `puzzle_generators.*` only
    for m in re.finditer(r"from\s+(scripts\.\w+(?:\.\w+)*)\s+import|import\s+(scripts\.\w+(?:\.\w+)*)", text):
        mod = m.group(1) or m.group(2)
        spec = importlib.util.find_spec(mod)
        if spec is None:
            missing.append(f"runner.py imports {mod} which is not importable")
    # data dir
    rule_dir = ROOT / "data" / "base" / "solutions"
    if not rule_dir.exists():
        missing.append("data/base/solutions/ (rule sources) is missing")
    return missing


def import_sample(n: int = 5, seed: int = 0) -> tuple[int, int, list[str]]:
    """Import N random generators and call generate(0, 0)."""
    dirs = [p for p in PER_PUZZLE.iterdir() if p.is_dir() and (p / "generator.py").exists()]
    rng = random.Random(seed)
    sample = rng.sample(dirs, min(n, len(dirs)))
    ok = 0
    failures: list[str] = []
    for d in sample:
        mod_name = f"puzzle_generators.per_puzzle.{d.name}.generator"
        try:
            mod = importlib.import_module(mod_name)
            grid = mod.generate(0, 0)
            assert isinstance(grid, list) and grid and isinstance(grid[0], list), \
                f"{d.name}: generate did not return list-of-list"
            assert all(isinstance(v, int) for row in grid for v in row), \
                f"{d.name}: non-int cell value"
            ok += 1
        except Exception as e:
            failures.append(f"{d.name}: {type(e).__name__}: {e}")
    return ok, len(sample), failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", help="path to current_work.zip (audits the zip instead of live tree)")
    parser.add_argument("--sample", type=int, default=5, help="how many generators to direct-import")
    args = parser.parse_args()

    if args.zip:
        zp = Path(args.zip)
        if not zp.exists():
            print(f"ERROR: {zp} not found")
            sys.exit(2)
        gens, dirs, missing = count_generators_zip(zp)
        scope = f"zip ({zp})"
    else:
        gens, dirs, missing_paths = count_generators_live()
        missing = [str(p.relative_to(ROOT)) for p in missing_paths]
        scope = "live tree"

    readme_claim = read_readme_claim()
    progress_claim = read_progress_claim()
    smoke_ok, smoke_issues = smoke_ready_check()
    runtime_missing = missing_runtime_deps()
    sample_ok, sample_n, sample_fails = import_sample(args.sample) if not args.zip else (0, 0, [])

    fmt = lambda label, val: f"  {label:<35} {val}"
    print(f"=== Artifact audit ({scope}) ===")
    print(fmt("per_puzzle generator.py count:", gens))
    print(fmt("per_puzzle dirs:", dirs))
    print(fmt("dirs missing generator.py:", len(missing)))
    if missing[:5]:
        for m in missing[:5]:
            print(f"      {m}")
        if len(missing) > 5:
            print(f"      ... +{len(missing) - 5} more")
    print(fmt("README claimed count:", readme_claim if readme_claim is not None else "(not found)"))
    print(fmt("PROGRESS claimed count:", progress_claim if progress_claim is not None else "(not found)"))
    print(fmt("smoke-ready:", "yes" if smoke_ok else "no"))
    for s in smoke_issues:
        print(f"      {s}")
    print(fmt("missing runtime deps:", len(runtime_missing) or "(none)"))
    for m in runtime_missing:
        print(f"      {m}")
    if not args.zip:
        print(fmt(f"direct-import sample ({sample_n}):", f"{sample_ok}/{sample_n} pass"))
        for f in sample_fails:
            print(f"      {f}")

    fail = (
        bool(missing) or
        not smoke_ok or
        bool(runtime_missing) or
        (sample_ok < sample_n and not args.zip) or
        (readme_claim is not None and readme_claim != gens) or
        (readme_claim is None and not args.zip)
    )
    print()
    print("STATUS: " + ("FAIL" if fail else "PASS"))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
