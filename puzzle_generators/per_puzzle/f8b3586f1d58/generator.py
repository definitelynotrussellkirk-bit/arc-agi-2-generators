"""Generator for arc_additional_puzzles_21_set5:E31.

Rule: sparse colored cells on the left half are mirrored across the
vertical center line; originals remain.

Combinatorial axes (8): grid_h/w, palette_kind, n_cells, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, all_on_centerline, full_right_half.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f8b3586f1d58"
VERSION = "1.1.0"
TASK_ID = "f8b3586f1d58"
SUMMARY = "Sparse colored cells are mirrored across the vertical center line while originals remain."

INVARIANTS = [
    "input cells are sparse",
    "cells are placed on the left half",
    "background is zero",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_cells", "all_on_centerline", "full_right_half")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_half",
                       "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 7, 11)
    n = ctx.draw_int("n_cells", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h) for c in range((w + 1) // 2)]
    rng.shuffle(positions)
    colors = list(ctx.draw_distinct_colors("colors", n=min(n, 9), exclude={0}))
    for i, (r, c) in enumerate(positions[:n]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid — nothing to mirror
        return g
    if name == "all_on_centerline":
        # all cells exactly on center column → mirror is identity
        mid = w // 2
        g[1][mid] = 4
        g[3][mid] = 6
        g[5][mid] = 8
        return g
    if name == "full_right_half":
        # cells already on right half — invariant violated
        for r, c, v in [(1, 6, 2), (3, 7, 3), (5, 8, 4)]:
            g[r][c] = v
        return g
    return g
