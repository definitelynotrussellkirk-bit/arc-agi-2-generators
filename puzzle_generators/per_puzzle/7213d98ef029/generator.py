"""Generator for 19b:m128 — build marker equality matrix.

Rule: input row 0 (excluding cell (0,0)) is the column-header strip;
input col 0 (excluding cell (0,0)) is the row-header strip. Output is
an (n_rows x n_cols) grid where output[i][j] = row[i] iff
row[i] == col[j], else 0.

Combinatorial axes (8): n_rows, n_cols, palette_kind, n_shared,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared, all_same_color, corner_marked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7213d98ef029"
VERSION = "1.1.0"
TASK_ID = "7213d98ef029"
SUMMARY = "5x6 input: header row + header column, interior is bg."

INVARIANTS = [
    "background is 0",
    "cell (0,0) is bg",
    "row 0 cells (1..w-1) are colored (header)",
    "col 0 cells (1..h-1) are colored (header)",
    "interior cells (r>=1, c>=1) are bg",
    "at least one row-header value appears in the col-header (so output != all-zero)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared", "all_same_color", "corner_marked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_rows":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "n_cols":         {"type": "int", "default": "rng 5..7", "valid": "3..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shared":       {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "header_axes",
                       "valid": "header_axes"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..9"},
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
        n_rows = ctx.draw_int("n_rows", 4, 4)
        n_cols = ctx.draw_int("n_cols", 5, 5)
    elif difficulty == "hard":
        n_rows = ctx.draw_int("n_rows", 5, 6)
        n_cols = ctx.draw_int("n_cols", 6, 7)
    else:
        n_rows = ctx.draw_int("n_rows", 4, 6)
        n_cols = ctx.draw_int("n_cols", 5, 7)
    rng = ctx.draw_rng("layout")
    h = n_rows + 1; w = n_cols + 1
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while True:
        col_headers = [rng.choice(palette) for _ in range(n_cols)]
        row_headers = [rng.choice(palette) for _ in range(n_rows)]
        if set(row_headers) & set(col_headers):
            for j, v in enumerate(col_headers):
                g[0][j + 1] = v
            for i, v in enumerate(row_headers):
                g[i + 1][0] = v
            return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_shared":
        # disjoint top/left palettes → output is all zeros, no signal
        for j, v in enumerate([2, 3, 4, 5, 6], start=1):
            if j < w: g[0][j] = v
        for i, v in enumerate([7, 8, 9, 7, 8], start=1):
            if i < h: g[i][0] = v
        return g
    if name == "all_same_color":
        # all top + all left share one color → output is full diag-grid match, no contrast
        for j in range(1, w):
            g[0][j] = 5
        for i in range(1, h):
            g[i][0] = 5
        return g
    if name == "corner_marked":
        # (0,0) non-zero → invariant violation, ambiguous header role
        g[0][0] = 7
        for j, v in enumerate([2, 3, 4, 5, 6], start=1):
            if j < w: g[0][j] = v
        for i, v in enumerate([2, 3, 4, 5, 6], start=1):
            if i < h: g[i][0] = v
        return g
    return g
