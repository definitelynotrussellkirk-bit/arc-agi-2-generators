"""Generator for arc_puzzle_bank_sixteenth_21_bundle:easy_107_complete_vertical_mirror.

Rule: sparse left-side cells are copied across the vertical center line.

Combinatorial axes (8): grid_h, half_w, palette_kind, cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, on_axis_only, already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a1f5c5bd7df9"
VERSION = "1.1.0"
TASK_ID = "a1f5c5bd7df9"
SUMMARY = "Sparse left-side cells are copied across the vertical center line."

INVARIANTS = [
    "background is 0",
    "grid has a vertical mirror axis",
    "source cells are placed on the left half",
    "mirrored target cells are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "on_axis_only", "already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..18"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "2..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 4..8", "valid": "1..30"},
    "palette_size":   {"type": "int", "default": "rng 1..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_half", "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..9", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        half_w = ctx.draw_int("half_w", 4, 5)
        target = ctx.draw_int("cells", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        half_w = ctx.draw_int("half_w", 5, 6)
        target = ctx.draw_int("cells", 6, 8)
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
    h, w = 8, 11
    axis = w // 2
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no cells to mirror — input equals output
        return g
    if name == "on_axis_only":
        # all sources on the vertical axis column → reflection is identity
        for r in [1, 3, 5, 6]:
            g[r][axis] = ((r % 7) + 1)
        return g
    if name == "already_symmetric":
        # pattern is already vertical-mirror symmetric → rule no-op
        for r, c in [(1, 1), (1, w - 2), (3, 3), (3, w - 4), (5, 0), (5, w - 1)]:
            g[r][c] = 4
        return g
    return g
