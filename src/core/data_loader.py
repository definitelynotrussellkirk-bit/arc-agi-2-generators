"""Load ARC-AGI-2 data from raw JSON files."""

import json, os
from pathlib import Path

# Primary: local repo data/raw/. Fallback: Kaggle competition mount.
_CANDIDATES = [
    Path(__file__).resolve().parents[2] / "data" / "raw",
    Path("/kaggle/input/competitions/arc-prize-2026-arc-agi-2"),
    Path("/kaggle/input/arc-prize-2026-arc-agi-2"),
]
DATA_DIR = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])


def load_challenges(dataset: str = "training") -> dict:
    """Load challenge tasks. dataset: 'training', 'evaluation', or 'test'."""
    fname = f"arc-agi_{dataset}_challenges.json"
    # Try each candidate directory — Kaggle mounts may differ from local
    for d in _CANDIDATES:
        path = d / fname
        if path.exists():
            with open(path) as f:
                return json.load(f)
    raise FileNotFoundError(f"{fname} not found in any of: {[str(d) for d in _CANDIDATES]}")


def load_solutions(dataset: str = "training") -> dict:
    """Load solutions. dataset: 'training' or 'evaluation'."""
    path = DATA_DIR / f"arc-agi_{dataset}_solutions.json"
    with open(path) as f:
        return json.load(f)


def load_task_pairs(dataset: str = "training") -> dict:
    """Load challenges merged with solutions (where available)."""
    challenges = load_challenges(dataset)
    try:
        solutions = load_solutions(dataset)
    except FileNotFoundError:
        solutions = {}

    merged = {}
    for task_id, task in challenges.items():
        merged[task_id] = {
            "train": task["train"],
            "test": task["test"],
        }
        if task_id in solutions:
            for i, sol in enumerate(solutions[task_id]):
                if i < len(merged[task_id]["test"]):
                    merged[task_id]["test"][i]["output"] = sol
    return merged
