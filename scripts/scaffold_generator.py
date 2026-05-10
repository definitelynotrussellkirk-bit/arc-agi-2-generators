#!/usr/bin/env python3
"""Print a fillable generator skeleton for a given task_id.

READ-ONLY. This script writes nothing to disk and creates no tasks.
It prints the rule body, structural hints, and a skeleton you can
copy into puzzle_generators/per_puzzle/<task_id>/generator.py and
fill in by hand.

Usage:
    python3 -m scripts.scaffold_generator <task_id>
    python3 -m scripts.scaffold_generator additional_bank:M5
    python3 -m scripts.scaffold_generator additional_bank:M5 --pattern frame_fill

Round-5 design constraint: this MUST stay a printer, not a writer.
The "no invented work / no bulk auto-rewrites" rules in CLAUDE.md
mean the generator file itself is hand-authored.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _read_canonical(task_id: str) -> dict | None:
    path = ROOT / "data" / "canonical" / "puzzles.jsonl"
    if not path.exists():
        return None
    with path.open() as f:
        for line in f:
            try:
                row = json.loads(line)
            except Exception:
                continue
            if row.get("task_id") == task_id:
                return row
    return None


def _read_difficulty(task_id: str) -> str | None:
    path = ROOT / "data" / "canonical" / "puzzle_db.jsonl"
    if not path.exists():
        return None
    with path.open() as f:
        for line in f:
            try:
                row = json.loads(line)
            except Exception:
                continue
            if row.get("task_id") == task_id:
                return row.get("difficulty")
    return None


# Heuristic structural tags by Racket primitives the rule mentions.
_TAG_RULES = [
    ("uses_objects",         re.compile(r"\(objects\s+g\b")),
    ("uses_objects_8",       re.compile(r"\(objects-8\b")),
    ("uses_objects_multicolor", re.compile(r"\(objects-multicolor\b")),
    ("uses_bbox",            re.compile(r"\bobj-bbox|bbox-of-cells")),
    ("uses_grid_from_fn",    re.compile(r"\(grid-from-fn\b")),
    ("uses_paint_cells",     re.compile(r"\(paint-cells\b")),
    ("uses_find_color",      re.compile(r"\(find-color\b")),
    ("uses_grid_colors",     re.compile(r"\(grid-colors\b")),
    ("uses_dihedral",        re.compile(r"rotate-cw|rotate-180|flip-lr|flip-ud|transpose")),
    ("uses_for_fold",        re.compile(r"for/fold|for\*/fold")),
    ("uses_bfs",             re.compile(r"connected-region|hash-set!|hash-has-key\?")),
    ("uses_cardinal_deltas", re.compile(r"\bcardinal-deltas\b")),
    ("uses_filter_cells",    re.compile(r"\(filter-cells\b")),
    ("mutates_state",        re.compile(r"\bset!|hash-set!")),
    ("uses_subgrid",         re.compile(r"\(subgrid\b")),
    ("uses_center_of_mass",  re.compile(r"center-of-mass")),
]


def _tag_rule(rule: str) -> list[str]:
    return [tag for tag, rx in _TAG_RULES if rx.search(rule)]


_PATTERN_HINTS = {
    "frame_fill": [
        "Place 1-2 rect frames in distinct colors via draw_frame.",
        "Each frame's interior holds a single marker cell.",
        "Frames don't touch each other (use bbox_overlaps).",
    ],
    "sort_pack": [
        "Place 2-3 objects with DISTINCT sizes (so the sort key is unambiguous).",
        "Each object in a distinct color.",
        "Use blobs.bbox_overlaps to keep them non-touching.",
    ],
    "marker_pair_connect": [
        "1-3 distinct colors; each color has EXACTLY 2 markers.",
        "Each pair shares a row OR a column with ≥1 0-cell between.",
        "Pairs use distinct rows AND distinct cols.",
    ],
    "stamp_anchor": [
        "Define a small template (3-5 cells) at a known anchor.",
        "Place 1-3 anchor cells elsewhere with room for the template.",
        "Margin = max(template_h, template_w) so stamps stay in-bounds.",
    ],
    "pick_crop": [
        "2-3 objects with one unambiguously-best (largest, most-holes, ...).",
        "If marker-color match: (0,0) holds the target color.",
    ],
    "recolor_by_property": [
        "N objects with DISTINCT property values (size / line-shape / hole count).",
        "Each in a distinct non-output color (avoid 1, 2, 3 if those are outputs).",
    ],
    "cmd_transform": [
        "(0,0) holds a cmd value (typically 1..4 or 2..6).",
        "Rest of grid is a motif the cmd transforms.",
        "Exclude cmd values from the motif palette.",
    ],
}


def _emit_skeleton(task_id: str, rule: str | None, difficulty: str | None,
                   tags: list[str], pattern: str | None) -> str:
    module_id = task_id.replace(":", "__").replace("-", "_")
    pattern_lines = []
    if pattern and pattern in _PATTERN_HINTS:
        pattern_lines = _PATTERN_HINTS[pattern]

    rule_block = ""
    if rule:
        truncated = rule if len(rule) <= 1500 else rule[:1500] + "\n... [truncated]"
        rule_block = f'"""\n{truncated}\n"""\n'

    pattern_str = pattern or "(none chosen)"
    diff_str = difficulty or "(unknown)"
    tag_str = ", ".join(tags) if tags else "(no tags detected)"
    invariants_block = "\n".join(f"#   - {h}" for h in pattern_lines) or \
                       "#   - (write your own — what does the generator's output need to satisfy?)"

    return f'''# === scaffold for {task_id} ===
# Difficulty: {diff_str}
# Pattern hint: {pattern_str}
# Rule tags: {tag_str}
#
# Rule body (for reference; canonical source is data/canonical/puzzles.jsonl):
{rule_block}#
# Invariants the generator must satisfy:
{invariants_block}
#
# Smoke this file with:
#   python3 scripts/sample_generator.py --tid {task_id} --smoke 5
#
# Save as:
#   puzzle_generators/per_puzzle/{module_id}/generator.py

"""Generator for {task_id} — <one-line summary of the rule>."""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at, fill_box, draw_frame
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "{module_id}"
VERSION = "1.0.0"
TASK_ID = "{task_id}"

SUMMARY = "<one-line summary>"

INVARIANTS = [
    "background is 0",
    # ... fill in
]

AXES = {{
    "grid_h": {{"type": "int", "default": "rng 8..12", "valid": "6..16"}},
    "grid_w": {{"type": "int", "default": "rng 10..14", "valid": "6..18"}},
}}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("grid_h", 8, 12)
    w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    # ... build the input grid here
    return g
'''


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    p.add_argument("task_id", type=str, help="Canonical task_id (e.g., 'additional_bank:M5')")
    p.add_argument("--pattern", choices=sorted(_PATTERN_HINTS),
                    help="Pattern from docs/GENERATOR_PATTERNS.md to seed the invariants block.")
    args = p.parse_args(argv)

    row = _read_canonical(args.task_id)
    if row is None:
        print(f"task_id not found in data/canonical/puzzles.jsonl: {args.task_id!r}",
              file=sys.stderr)
        return 1

    rule = row.get("program_solution") or ""
    difficulty = _read_difficulty(args.task_id)
    tags = _tag_rule(rule) if rule else []

    print(_emit_skeleton(args.task_id, rule, difficulty, tags, args.pattern))
    return 0


if __name__ == "__main__":
    sys.exit(main())
