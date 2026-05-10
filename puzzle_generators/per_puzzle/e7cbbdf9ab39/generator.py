"""Generator for 7b:m43 — marked rowcol crossings.

Rule: column markers (color 3) on top+bottom borders pair up; row
markers (color 2) on left+right borders pair up. At every (row,col)
crossing of paired markers, place an 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cols, n_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: unpaired_col, unpaired_row, no_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e7cbbdf9ab39"
VERSION = "1.1.0"
TASK_ID = "e7cbbdf9ab39"
SUMMARY = "Pairs of column markers (3) on top+bottom + row markers (2) on left+right."

INVARIANTS = [
    "background is 0",
    "1-3 columns have a 3 in row 0 AND row h-1",
    "1-3 rows have a 2 in col 0 AND col w-1",
    "the row markers are not on the top/bottom edge rows",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("unpaired_col", "unpaired_row", "no_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cols":         {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "n_rows":         {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "border_pairs",
                       "valid": "border_pairs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_cols = rng.randint(1, 3)
    n_rows = rng.randint(1, 3)
    cols = rng.sample(range(2, w - 2), n_cols)
    rows = rng.sample(range(2, h - 2), n_rows)
    for c in cols:
        g[0][c] = 3; g[h - 1][c] = 3
    for r in rows:
        g[r][0] = 2; g[r][w - 1] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "unpaired_col":
        # column 3 only on top, missing on bottom → no pair, no crossing
        g[0][3] = 3
        g[3][0] = 2; g[3][w - 1] = 2
        return g
    if name == "unpaired_row":
        # row 2 only on left, missing on right → no pair, no crossing
        g[0][3] = 3; g[h - 1][3] = 3
        g[3][0] = 2
        return g
    if name == "no_markers":
        # blank → no crossings, output identical to input
        return g
    return g
