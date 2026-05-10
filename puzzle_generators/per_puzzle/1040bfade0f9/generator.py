"""Generator for 6b:m41 — color equality matrix.

Rule: row 0 holds top header colors (skip col 0); col 0 holds left
header colors (skip row 0). Output: at (r, c), if left[r] == top[c]
output that color, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shared,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared, headers_all_same, missing_one_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1040bfade0f9"
VERSION = "1.1.0"
TASK_ID = "1040bfade0f9"
SUMMARY = "Top + left headers with some overlapping colors."

INVARIANTS = [
    "background is 0 in body",
    "row 0 has colors from col 1+ (top header)",
    "col 0 has colors from row 1+ (left header)",
    "top + left share >=1 color (so output has matches)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared", "headers_all_same", "missing_one_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
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
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
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
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_shared":
        # disjoint top/left palettes → output is all zeros, no signal
        top = [2, 3, 4, 5, 6]
        left = [7, 8, 9, 7, 8]
        for c, color in enumerate(top, start=1):
            if c < w: g[0][c] = color
        for r, color in enumerate(left, start=1):
            if r < h: g[r][0] = color
        return g
    if name == "headers_all_same":
        # all headers share one color → output is full grid match, no contrast
        for c in range(1, w):
            g[0][c] = 5
        for r in range(1, h):
            g[r][0] = 5
        return g
    if name == "missing_one_axis":
        # only top header present, left axis empty → no row-color to compare against
        for c, color in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = color
        return g
    return g
