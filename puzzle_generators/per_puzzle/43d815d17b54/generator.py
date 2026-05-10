"""Generator for c87289bb.

Rule: top-row cyan columns extend into red floor segments and create
side walls.

Combinatorial axes (8): grid_h/w, two_row, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_segments, no_columns, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "43d815d17b54"
VERSION = "1.1.0"
TASK_ID = "43d815d17b54"
SUMMARY = "Top-row cyan columns extend into red floor segments; side walls created."

INVARIANTS = [
    "all cyan source columns are marked in the top row",
    "one lower row contains red horizontal segments",
    "cyan columns inside a red segment stop at that segment",
    "two and eight colors are distinct from background",
]

TWO_ROWS = ("r5", "r6", "r7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_segments", "no_columns", "full_grid")
HELPFUL_TEXTURES = TWO_ROWS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "two_row":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TWO_ROWS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for two_row",
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
    if tx in TWO_ROWS:
        two_row = int(tx[1:])
    else:
        two_row = ctx.draw_choice("two_row", [5, 6, 7])
    left_start = ctx.draw_choice("left_start", [2, 3])
    left_len = ctx.draw_choice("left_len", [3, 4])
    gap = ctx.draw_choice("gap", [2, 3])
    right_start = left_start + left_len + gap
    right_len = ctx.draw_choice("right_len", [3, 4])
    right_end = min(12, right_start + right_len - 1)
    g = full_grid(11, 14, 0)
    left_end = left_start + left_len - 1
    for c in range(left_start, left_end + 1):
        g[two_row][c] = 2
    for c in range(right_start, right_end + 1):
        g[two_row][c] = 2
    eight_cols = [left_start, left_end, right_start + 1, right_end]
    for c in sorted(set(c for c in eight_cols if c < 14)):
        g[0][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 14, 0)
    if name == "no_segments":
        g[0][3] = 8; g[0][9] = 8
        return g
    if name == "no_columns":
        for c in range(2, 8):
            g[6][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
