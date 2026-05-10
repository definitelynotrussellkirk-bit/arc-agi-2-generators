"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_127_complete_horizontal_mirror.

Rule: scatter upper-half cells whose horizontal mirror copies are
empty are copied across the horizontal axis.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, lower_half_only, already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0c023af8384a"
VERSION = "1.1.0"
TASK_ID = "0c023af8384a"
SUMMARY = "Scatter upper-half cells whose horizontal mirror copies are empty."

INVARIANTS = [
    "background is 0",
    "all source cells are off the horizontal mirror axis",
    "mirrored target cells are initially empty",
    "original colors are preserved after copying",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "lower_half_only", "already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 3..7", "valid": "1..24"},
    "palette_size":   {"type": "int", "default": "rng 1..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_half", "valid": "upper_half"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("cells", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("cells", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        target = ctx.draw_int("cells", 3, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    candidates = [(r, c) for r in range(h // 2) for c in range(w)]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no cells to mirror — input equals output
        return g
    if name == "lower_half_only":
        # all sources in the lower half → upper-half-source assumption violated
        for r, c in [(5, 1), (6, 4), (7, 7)]:
            g[r][c] = 3
        return g
    if name == "already_symmetric":
        # pattern is already horizontal-mirror symmetric → rule has no visible effect
        for r, c in [(1, 2), (h - 1 - 1, 2), (2, 5), (h - 1 - 2, 5)]:
            g[r][c] = 4
        return g
    return g
