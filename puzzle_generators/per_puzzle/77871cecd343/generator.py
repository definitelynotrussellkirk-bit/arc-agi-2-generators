"""Generator for arc_additional_puzzle_bank_volume21:M147 — Reflect 1-cells across 9-axes to 8.

Rule: 9-row + 9-col split grid into 4 quadrants. For each 1-cell, reflect
across both axes; paint 8 at 3 reflected positions if in bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axes, one_axis_only, cells_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "77871cecd343"
VERSION = "1.1.0"
TASK_ID = "77871cecd343"
SUMMARY = "9-row and 9-col axes + 1-2 1-cells in upper-left quadrant."

INVARIANTS = [
    "exactly one full-row 9-axis and one full-column 9-axis",
    "1-2 1-cells in upper-left quadrant",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axes", "one_axis_only", "cells_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "ul_quad_with_9_cross_axes",
                       "valid": "ul_quad_with_9_cross_axes"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sep_r = h // 2
    sep_c = w // 2
    for c in range(w):
        g[sep_r][c] = 9
    for r in range(h):
        g[r][sep_c] = 9
    n = rng.randint(1, 2)
    for _ in range(n * 5):
        r = rng.randint(0, sep_r - 1)
        c = rng.randint(0, sep_c - 1)
        if g[r][c] == 0:
            g[r][c] = 1; n -= 1
            if n <= 0: break
    if rng.random() < 0.4:
        g[0][0] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    sep_r = h // 2
    sep_c = w // 2
    if name == "no_axes":
        # 1-cells but no 9-axes → reflection axes undefined
        g[1][2] = 1; g[2][3] = 1
        return g
    if name == "one_axis_only":
        # only the row 9-axis (no col 9) → can only reflect across one axis
        for c in range(w): g[sep_r][c] = 9
        g[1][2] = 1; g[2][3] = 1
        return g
    if name == "cells_on_axis":
        # 1-cells on the 9-axis → reflection collapses (cell reflects to itself)
        for c in range(w): g[sep_r][c] = 9
        for r in range(h): g[r][sep_c] = 9
        g[sep_r][2] = 1   # on row-axis (will overwrite the 9 marker)
        g[2][sep_c] = 1   # on col-axis (will overwrite the 9 marker)
        return g
    return g
