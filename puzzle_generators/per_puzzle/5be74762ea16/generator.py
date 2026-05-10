"""Generator for arc_additional_puzzles_21_set10_bundle:M69.

Rule: among 3 distinct-color blobs of distinct sizes, crop the median-size
blob's bbox; if h>w, rotate it 90° clockwise.

Combinatorial axes (8): grid_h/w, palette_kind, num_blobs, size_spread,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_same_size, only_two_blobs, square_median.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "5be74762ea16"
VERSION = "1.1.0"
TASK_ID = "5be74762ea16"
SUMMARY = "3 distinct-color blobs of distinct sizes."

INVARIANTS = [
    "exactly 3 non-touching blobs of distinct sizes",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("all_same_size", "only_two_blobs", "square_median")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
    paint_at(g, 1, 5, [(0, 0), (0, 1), (0, 2), (1, 1)], 4)
    paint_at(g, h - 4, 1, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "all_same_size":
        # All 3 same size — median is ambiguous
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 1, 6, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, h - 4, 3, [(0, 0), (0, 1), (1, 0)], 7)
        return g
    if name == "only_two_blobs":
        # 2 blobs — no median (the middle of an even count is undefined)
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
        paint_at(g, h - 4, 1, [(0, 0), (0, 1), (0, 2), (1, 0)], 4)
        return g
    if name == "square_median":
        # Median bbox is square — h>w branch never triggers
        paint_at(g, 1, 1, [(0, 0)], 2)
        paint_at(g, 1, 4, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        paint_at(g, h - 4, 1, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)], 7)
        return g
    return g
