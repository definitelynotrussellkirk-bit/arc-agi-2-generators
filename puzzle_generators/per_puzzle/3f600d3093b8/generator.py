"""Generator for arc_additional_puzzles_21_set8:M54.

Rule: row 0 and col 0 mark interesting rows/cols with 8s; rule extracts
the marked sub-matrix.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_row_markers,
n_col_markers, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_row_markers, no_col_markers, blank_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3f600d3093b8"
VERSION = "1.1.0"
TASK_ID = "3f600d3093b8"
SUMMARY = "Row 0 and col 0 mark interesting rows/cols with 8s; rule extracts the marked sub-matrix."

INVARIANTS = [
    ">=2 row markers (cells (r, 0) == 8 for r >= 1)",
    ">=2 col markers (cells (0, c) == 8 for c >= 1)",
    "cell (0, 0) is bg or any value (the rule doesn't read it specifically)",
    "interior cells (r >= 1, c >= 1) are filled with various non-bg, non-8 colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_row_markers", "no_col_markers", "blank_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_row_markers":  {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "n_col_markers":  {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "row0_col0_markers",
                       "valid": "row0_col0_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "scattered", "valid": "scattered"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_row = ctx.draw_int("n_row_markers", 2, 2)
        n_col = ctx.draw_int("n_col_markers", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_row = ctx.draw_int("n_row_markers", 3, 4)
        n_col = ctx.draw_int("n_col_markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_row = ctx.draw_int("n_row_markers", 2, 4)
        n_col = ctx.draw_int("n_col_markers", 2, 4)
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    rows_with_marker = rng.sample(range(1, h), n_row)
    for r in rows_with_marker:
        g[r][0] = 8
    cols_with_marker = rng.sample(range(1, w), n_col)
    for c in cols_with_marker:
        g[0][c] = 8

    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0, 8})
    rng2 = ctx.draw_rng("content")
    for r in range(1, h):
        for c in range(1, w):
            if rng2.random() < 0.5:
                g[r][c] = rng2.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_row_markers":
        # only col-markers in row 0, no rows marked → output sub-matrix has 0 rows
        for c in [2, 5, 7]: g[0][c] = 8
        for r in range(1, h):
            for c in range(1, w):
                if (r + c) % 3 == 0:
                    g[r][c] = (c % 6) + 1
        return g
    if name == "no_col_markers":
        # only row-markers in col 0, no cols marked → output sub-matrix has 0 cols
        for r in [2, 5, 7]: g[r][0] = 8
        for r in range(1, h):
            for c in range(1, w):
                if (r + c) % 3 == 0:
                    g[r][c] = (c % 6) + 1
        return g
    if name == "blank_interior":
        # markers present but interior all bg → output sub-matrix is all 0
        for r in [2, 5]: g[r][0] = 8
        for c in [3, 6]: g[0][c] = 8
        return g
    return g
