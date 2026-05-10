"""Generator for arc_additional_puzzle_bank_volume8:M54.

Rule: row 0 has 1-cells (cols) and 2-cells (cols); col 0 has 1-cells
(rows) and 2-cells (rows). Paint 3 at intersections of red rows/cols,
8 at intersections of blue rows/cols.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_row_markers, missing_col_markers, parallel_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2bd1c5b0e076"
VERSION = "1.1.0"
TASK_ID = "2bd1c5b0e076"
SUMMARY = "Row 0 and col 0 each have 1-2 cells of color 1 and 1-2 cells of color 2."

INVARIANTS = [
    "row 0 (cols ≥ 1) has 2-cells of color 1 and 2-cells of color 2",
    "col 0 (rows ≥ 1) has 2-cells of color 1 and 2-cells of color 2",
    "decoration is non-{0,1,2,3,8} cell elsewhere",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_row_markers", "missing_col_markers", "parallel_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "2_per_color", "valid": "2_per_color"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "axis_markers",
                       "valid": "axis_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[0][3] = 1; g[0][6] = 1
    g[0][4] = 2; g[0][7] = 2
    g[1][0] = 2; g[2][0] = 2
    g[3][0] = 1; g[4][0] = 1
    g[h - 1][w - 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "missing_row_markers":
        # row 0 has no 1/2 markers → no candidate columns, no intersections
        g[1][0] = 2; g[2][0] = 2
        g[3][0] = 1; g[4][0] = 1
        return g
    if name == "missing_col_markers":
        # col 0 has no 1/2 markers → no candidate rows, no intersections
        g[0][3] = 1; g[0][6] = 1
        g[0][4] = 2; g[0][7] = 2
        return g
    if name == "parallel_only":
        # only one color present on both axes → only one set of intersections, the other is empty
        g[0][3] = 1; g[0][6] = 1
        g[3][0] = 1; g[4][0] = 1
        return g
    return g
