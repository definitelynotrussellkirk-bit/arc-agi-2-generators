"""Generator for arc_additional_puzzles_21_set14_bundle:M92 — Checkerboard alternating row/col keys.

Rule: row-keys = col 0 values (rows 1+); col-keys = row 0 values
(cols 1+). Output is 2N × 2M where (r,c) is row-key[r//2] if (r+c)
even, col-key[c//2] otherwise.

Combinatorial axes (8): n_rows, n_cols, palette_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_row_keys, missing_col_keys, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ca9ccc338509"
VERSION = "1.1.0"
TASK_ID = "ca9ccc338509"
SUMMARY = "Row 0 + col 0 hold key palettes; output is 2N×2M checkerboard alternating row/col keys."

INVARIANTS = [
    "row 0 (cols 1+) holds 1..3 distinct color values",
    "col 0 (rows 1+) holds 1..3 distinct color values",
    "(0,0) is 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_row_keys", "missing_col_keys", "all_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "n_cols":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "row0_col0_keys",
                       "valid": "row0_col0_keys"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
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
        n_rows = ctx.draw_int("n_rows", 2, 2)
        n_cols = ctx.draw_int("n_cols", 2, 2)
    elif difficulty == "hard":
        n_rows = ctx.draw_int("n_rows", 3, 3)
        n_cols = ctx.draw_int("n_cols", 3, 3)
    else:
        n_rows = ctx.draw_int("n_rows", 2, 3)
        n_cols = ctx.draw_int("n_cols", 2, 3)
    h = n_rows + 1; w = n_cols + 1
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color_rng = ctx.draw_rng("colors")
    for r in range(1, h):
        g[r][0] = color_rng.randint(1, 9)
    for c in range(1, w):
        g[0][c] = color_rng.randint(1, 9)
    return g


def _draw_from_degenerate(name, rng):
    if name == "missing_row_keys":
        # col 0 (rows 1+) is blank → no row-key palette; checkerboard's "even" cells are 0
        h, w = 4, 4
        g = full_grid(h, w, 0)
        g[0][1] = 4; g[0][2] = 6; g[0][3] = 3
        # col 0 stays blank
        return g
    if name == "missing_col_keys":
        # row 0 (cols 1+) is blank → no col-key palette; checkerboard's "odd" cells are 0
        h, w = 4, 4
        g = full_grid(h, w, 0)
        # row 0 stays blank
        g[1][0] = 4; g[2][0] = 6; g[3][0] = 3
        return g
    if name == "all_same_color":
        # all keys identical → output checkerboard collapses to a uniform color (no pattern)
        h, w = 4, 4
        g = full_grid(h, w, 0)
        for c in range(1, w): g[0][c] = 5
        for r in range(1, h): g[r][0] = 5
        return g
    return full_grid(4, 4, 0)
