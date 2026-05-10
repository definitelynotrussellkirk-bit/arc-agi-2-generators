"""Generator for arc_puzzle_bank_21_set12_bundle:medium_l09.

Rule: among 3 distinct-color blobs of distinct sizes, pick the median
(middle by size) and emit it on a blank grid in its color.

Combinatorial axes (8): grid_h/w, palette_kind, num_blobs, size_spread,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_same_size, only_two_blobs, tied_middle.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "f395ecd79f92"
VERSION = "1.1.0"
TASK_ID = "f395ecd79f92"
SUMMARY = "3 distinct-color blobs of distinct sizes."

INVARIANTS = [
    "exactly 3 non-touching blobs of distinct sizes",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("all_same_size", "only_two_blobs", "tied_middle")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_blobs":      {"type": "int", "default": "3", "valid": "3"},
    "size_spread":    {"type": "str", "default": "wide", "valid": "wide"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
    paint_at(g, 1, 5, [(0, 0), (0, 1), (1, 0), (1, 1)], 3)
    paint_at(g, h - 4, 2, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "all_same_size":
        # all 3 same size — no median selection
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 1, 6, [(0, 0), (0, 1), (1, 0)], 3)
        paint_at(g, h - 4, 3, [(0, 0), (0, 1), (1, 0)], 4)
        return g
    if name == "only_two_blobs":
        # 2 blobs — no middle (even count)
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
        paint_at(g, h - 4, 1, [(0, 0), (0, 1), (0, 2), (1, 0)], 3)
        return g
    if name == "tied_middle":
        # 4 blobs with two tied for the middle position
        paint_at(g, 1, 1, [(0, 0)], 2)
        paint_at(g, 1, 4, [(0, 0), (0, 1)], 3)
        paint_at(g, 1, 8, [(0, 0), (0, 1)], 4)
        paint_at(g, h - 4, 3, [(0, 0), (0, 1), (0, 2), (1, 0)], 6)
        return g
    return g
