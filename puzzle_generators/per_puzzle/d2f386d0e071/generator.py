"""Generator for arc_puzzle_bank_tenth_21_bundle:easy_65_complete_vertical_mirror.

Rule: sparse left-half cells are copied across the vertical grid axis.

Combinatorial axes (8): grid_h, half_w, palette_kind, cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_left, full_left, source_in_right.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d2f386d0e071"
VERSION = "1.1.0"
TASK_ID = "d2f386d0e071"
SUMMARY = "Sparse left-half cells are copied across the vertical grid axis."

INVARIANTS = [
    "background is 0",
    "grid width is odd",
    "source cells are in the left half",
    "mirrored cells are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_left", "full_left", "source_in_right")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..18"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "2..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 4..8", "valid": "1..30"},
    "palette_size":   {"type": "int", "default": "rng 1..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_half", "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..6", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        half_w = ctx.draw_int("half_w", 4, 5)
        target = ctx.draw_int("cells", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        half_w = ctx.draw_int("half_w", 5, 6)
        target = ctx.draw_int("cells", 6, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        half_w = ctx.draw_int("half_w", 4, 6)
        target = ctx.draw_int("cells", 4, 8)
    w = half_w * 2 + 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    candidates = [(r, c) for r in range(h) for c in range(half_w)]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, half_w = 8, 5
    w = half_w * 2 + 1
    g = full_grid(h, w, 0)
    if name == "empty_left":
        # nothing on left → mirror produces empty right; rule is no-op
        return g
    if name == "full_left":
        # every left cell filled → output is fully painted (no bg cells)
        for r in range(h):
            for c in range(half_w):
                g[r][c] = ((r + c) % 7) + 1
        return g
    if name == "source_in_right":
        # source cells live in the right half — invariant violated
        for r, c in [(1, w - 2), (3, w - 3), (5, w - 1)]:
            g[r][c] = 4
        return g
    return g
