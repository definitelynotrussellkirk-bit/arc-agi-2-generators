"""Generator for v3_rich_schema:easy_04_intersections_from_markers — paint intersections.

Rule: row 0 has color-1 markers at some columns; column 0 has color-2
markers at some rows. Output paints color 4 at every (r, c) where
both markers exist.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_col, n_row,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_col_markers, no_row_markers, marker_color_swap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c5d56d92f343"
VERSION = "1.1.0"
TASK_ID = "c5d56d92f343"
SUMMARY = "Row 0 has color-1 column markers + column 0 has color-2 row markers."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 color-1 markers at distinct columns ≥ 1",
    "column 0 has 2-3 color-2 markers at distinct rows ≥ 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_col_markers", "no_row_markers", "marker_color_swap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_col":          {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "n_row":          {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "row0_col0_markers",
                       "valid": "row0_col0_markers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        n_col = ctx.draw_int("n_col", 2, 2)
        n_row = ctx.draw_int("n_row", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n_col = ctx.draw_int("n_col", 3, 3)
        n_row = ctx.draw_int("n_row", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
        n_col = ctx.draw_int("n_col", 2, 3)
        n_row = ctx.draw_int("n_row", 2, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    cols = rng.sample(range(1, w), n_col)
    for c in cols:
        g[0][c] = 1
    rows = rng.sample(range(1, h), n_row)
    for r in rows:
        g[r][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_col_markers":
        # only row markers, no column markers → no intersections, output has no 4s
        for r in [2, 4, 5]: g[r][0] = 2
        return g
    if name == "no_row_markers":
        # only column markers, no row markers → no intersections, output has no 4s
        for c in [2, 4, 6]: g[0][c] = 1
        return g
    if name == "marker_color_swap":
        # row markers use color 2 in row 0, col markers use color 1 in col 0 (swapped roles)
        for c in [2, 5]: g[0][c] = 2   # wrong color in row 0
        for r in [2, 4]: g[r][0] = 1   # wrong color in col 0
        return g
    return g
