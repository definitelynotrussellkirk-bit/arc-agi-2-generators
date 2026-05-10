"""Generator for arc_puzzle_bank_thirteenth21:E91 — mirror non-9 cells across row 9-axis.

Rule: rows with a 9 axis mirror their colored cells across that axis.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, mirror_already_filled, cells_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc68d333e854"
VERSION = "1.1.0"
TASK_ID = "fc68d333e854"
SUMMARY = "Rows with a 9 axis mirror their colored cells across that axis."

INVARIANTS = [
    "background is 0",
    "each active row contains exactly one 9 axis marker",
    "non-9 colored cells sit on one side of the row axis",
    "mirror destinations are initially blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "mirror_already_filled", "cells_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rows":           {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row_9axis_one_side_cells",
                       "valid": "row_9axis_one_side_cells"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("rows", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("rows", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("rows", 2, 3)
    target = min(target, h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 7, 8]
    for r in rng.sample(range(h), target):
        axis = rng.randint(3, w - 4)
        g[r][axis] = 9
        count = rng.randint(1, 2)
        offsets = rng.sample(range(1, min(axis + 1, w - axis)), count)
        side = rng.choice([-1, 1])
        for i, offset in enumerate(offsets):
            c = axis + side * offset
            g[r][c] = palette[(r + i + sample_index) % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # cells but no 9-axis in any row → no mirror line
        g[1][2] = 4; g[3][3] = 6
        return g
    if name == "mirror_already_filled":
        # mirror destination already has cells → mirror would clobber
        axis = w // 2
        g[1][axis] = 9
        g[1][axis - 2] = 4   # left
        g[1][axis + 2] = 6   # right (clobber target)
        return g
    if name == "cells_both_sides":
        # cells on both sides of axis → "one side" precondition fails
        axis = w // 2
        g[2][axis] = 9
        g[2][axis - 2] = 4
        g[2][axis + 1] = 6
        g[2][axis + 3] = 3
        return g
    return g
