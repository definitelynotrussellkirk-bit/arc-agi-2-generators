"""Generator for 4522001f.

Rule: 3x3 mini-grid with one empty row and column selects diagonal 4x4
output blocks from the red marker quadrant.

Combinatorial axes (8): grid_h/w, gap_row, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
block_color.
Degenerates: no_red, no_block, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ab4fcb302d2"
VERSION = "1.1.0"
TASK_ID = "0ab4fcb302d2"
SUMMARY = "3x3 mini-grid with one empty row and column; red marker selects blocks."

INVARIANTS = [
    "input is a 3x3 grid",
    "exactly one row and one column are all background",
    "one red marker sits in a non-gap quadrant",
    "the remaining non-gap cells carry one nonzero non-red color",
]

GAP_ROWS = ("g0", "g1", "g2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_red", "no_block", "full_grid")
HELPFUL_TEXTURES = GAP_ROWS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3"},
    "grid_w":         {"type": "int", "default": "3", "valid": "3"},
    "gap_row":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(GAP_ROWS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "block_color":    {"type": "color", "default": "rng !{0,2}",
                       "valid": "1|3|4|5|6|7|8|9"},
    "texture":        {"type": "str", "default": "alias for gap_row",
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
    if tx in GAP_ROWS:
        zero_r = int(tx[1])
    else:
        zero_r = ctx.draw_int("gap_row", 0, 2)
    zero_c = (seed * 2 + sample_index + rng.randint(0, 2)) % 3
    color = ctx.draw_color("block_color", exclude={0, 2})
    g = full_grid(3, 3, 0)
    rows = [r for r in range(3) if r != zero_r]
    cols = [c for c in range(3) if c != zero_c]
    red_index = (seed + sample_index + rng.randint(0, 3)) % 4
    cells = [(r, c) for r in rows for c in cols]
    for i, (r, c) in enumerate(cells):
        g[r][c] = 2 if i == red_index else color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 3, 0)
    if name == "no_red":
        g[0][0] = 3; g[2][2] = 3
        return g
    if name == "no_block":
        g[1][1] = 2
        return g
    if name == "full_grid":
        for r in range(3):
            for c in range(3):
                g[r][c] = 2
        return g
    return g
