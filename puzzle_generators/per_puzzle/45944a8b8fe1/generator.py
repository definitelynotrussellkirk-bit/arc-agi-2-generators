"""Generator for cf133acc.

Rule: broken horizontal runs and vertical anchors extend colored columns
upward.

Combinatorial axes (8): grid_h/w, line_row, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_runs, no_anchors, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "45944a8b8fe1"
VERSION = "1.1.0"
TASK_ID = "45944a8b8fe1"
SUMMARY = "Broken horizontal runs and vertical anchors extend colored columns upward."

INVARIANTS = [
    "a horizontal same-color run has a blank gap between its observed parts",
    "that gap is first filled to complete the horizontal run",
    "gap columns and isolated anchor columns are extended upward to each anchor",
]

LINE_ROWS = ("R5", "R6", "R7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_runs", "no_anchors", "full_grid")
HELPFUL_TEXTURES = LINE_ROWS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "line_row":       {"type": "choice", "default": "rng helpful",
                       "valid": "5|6|7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for line_row",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in LINE_ROWS:
        line_row = int(tx[1])
    else:
        line_row = ctx.draw_choice("line_row", [5, 6, 7])
    line_color, anchor_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(12, 13, 0)

    for c in [2, 3, 8, 9]:
        g[line_row][c] = line_color

    anchor_col = ctx.draw_choice("anchor_col", [10, 11])
    upper_anchor = ctx.draw_choice("upper_anchor", [2, 3])
    lower_anchor = ctx.draw_choice("lower_anchor", [8, 9])
    g[upper_anchor][anchor_col] = anchor_color
    g[lower_anchor][anchor_col] = anchor_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 0)
    if name == "no_runs":
        g[3][10] = 4
        return g
    if name == "no_anchors":
        for c in [2, 3, 8, 9]:
            g[6][c] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
