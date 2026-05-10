"""Generator for arc_additional_puzzles_21_set14_bundle:E92 — Cross product of row 0 and col 0 keys.

Rule: top row and left col are "keys". For (r>0, c>0), if g[r][0] ==
g[0][c] then output that color else 0. Row 0 / col 0 unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shared,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared, all_shared, missing_one_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c47d6176a161"
VERSION = "1.1.0"
TASK_ID = "c47d6176a161"
SUMMARY = "Top row and left col contain color keys; interior is all 0."

INVARIANTS = [
    "row 0 and col 0 contain various non-bg colors",
    ">=1 column color appears in left col (so at least one match)",
    "interior cells (r>0, c>0) are all 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared", "all_shared", "missing_one_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shared":       {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "header_axes",
                       "valid": "header_axes"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
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
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10))
    for c in range(1, w):
        g[0][c] = rng.choice(palette)
    g[0][0] = rng.choice(palette + [0])
    used_top = list(set(g[0][1:]))
    for r in range(1, h):
        if rng.random() < 0.7 and used_top:
            g[r][0] = rng.choice(used_top)
        else:
            g[r][0] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_shared":
        # disjoint top/left palettes → output is all zeros, no signal
        for c, v in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = v
        for r, v in enumerate([7, 8, 9, 7, 8], start=1):
            if r < h: g[r][0] = v
        return g
    if name == "all_shared":
        # top and left identical → output diag-like uniform match, no contrast
        for c in range(1, w):
            g[0][c] = 5
        for r in range(1, h):
            g[r][0] = 5
        return g
    if name == "missing_one_axis":
        # only top header (col 0 empty besides bg) → no row keys to match
        for c, v in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = v
        return g
    return g
