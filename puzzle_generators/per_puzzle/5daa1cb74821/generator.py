"""Generator for 20b:m135 — row/col color-match map.

Rule: row 0 has top legend (one color per col), col 0 has left legend
(one color per row). Output: at every (r, c), if left[r] == top[c]
and non-zero → that color, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shared,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared, headers_all_same, missing_one_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5daa1cb74821"
VERSION = "1.1.0"
TASK_ID = "5daa1cb74821"
SUMMARY = "Row 0 + col 0 hold legend strips; some row-col pairs match."

INVARIANTS = [
    "background is 0 in cells (r>=1, c>=1)",
    "(0,0) is 0",
    "row 0 cols >= 1 hold a sequence of distinct colors",
    "col 0 rows >= 1 hold a sequence of colors (some matching row 0)",
    ">=1 (left[r] == top[c]) match exists",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared", "headers_all_same", "missing_one_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shared":       {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "header_axes",
                       "valid": "header_axes"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 5, 6, 7]
    rng.shuffle(palette)
    top = [rng.choice(palette) for _ in range(w - 1)]
    left = [rng.choice(palette) for _ in range(h - 1)]
    if not any(l in top for l in left):
        left[0] = top[0]
    for c, color in enumerate(top, start=1):
        g[0][c] = color
    for r, color in enumerate(left, start=1):
        g[r][0] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_shared":
        # disjoint top/left palettes → output is all zeros, no signal
        for c, v in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = v
        for r, v in enumerate([7, 8, 9, 7, 8], start=1):
            if r < h: g[r][0] = v
        return g
    if name == "headers_all_same":
        # all headers share one color → output full match, no contrast
        for c in range(1, w):
            g[0][c] = 5
        for r in range(1, h):
            g[r][0] = 5
        return g
    if name == "missing_one_axis":
        # only top header, left axis empty → no row keys to match
        for c, v in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = v
        return g
    return g
