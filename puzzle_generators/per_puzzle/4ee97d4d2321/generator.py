"""Generator for arc_puzzle_bank_seventh_21_bundle:easy_44_mirror_across_cyan_axis.

Rule: a full cyan column is the mirror axis for sparse colored cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, cells_on_both_sides, axis_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4ee97d4d2321"
VERSION = "1.1.0"
TASK_ID = "4ee97d4d2321"
SUMMARY = "A full cyan column is the mirror axis for sparse colored cells."

INVARIANTS = [
    "background is 0",
    "exactly one full column is color 8",
    "non-axis cells are placed on one side of the axis",
    "their reflected positions are in bounds and initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "cells_on_both_sides", "axis_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 3..7", "valid": "1..24"},
    "palette_size":   {"type": "int", "default": "rng 3..7", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_of_axis",
                       "valid": "left_of_axis"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..7", "valid": "1..8"},
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
        half_w = ctx.draw_int("half_w", 4, 4)
        target = ctx.draw_int("cells", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        half_w = ctx.draw_int("half_w", 5, 6)
        target = ctx.draw_int("cells", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        half_w = ctx.draw_int("half_w", 4, 6)
        target = ctx.draw_int("cells", 3, 7)
    w = half_w * 2 + 1
    axis = half_w
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][axis] = 8
    candidates = [(r, c) for r in range(h) for c in range(axis)]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # cells but no cyan axis column → rule has no mirror line
        g[1][2] = 3; g[3][1] = 5; g[5][3] = 7
        return g
    if name == "cells_on_both_sides":
        # cells on both sides of axis → reflection would overwrite existing cells
        axis = 4
        for r in range(h): g[r][axis] = 8
        g[2][1] = 4; g[4][2] = 6
        g[2][7] = 5; g[4][6] = 7
        return g
    if name == "axis_at_edge":
        # axis at column 0 → no left side to mirror from
        for r in range(h): g[r][0] = 8
        g[2][3] = 4; g[4][5] = 6
        return g
    return g
