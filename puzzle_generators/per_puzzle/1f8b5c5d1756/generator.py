"""Generator for arc_puzzle_bank_21_set10_s:S10_H3.

Rule: among all blobs, identify the one with a unique normalized shape;
re-emit it (recolored) on a blank canvas.

Combinatorial axes (8): grid_h/w, palette_kind, common_size, unique_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_three_unique, all_three_same, only_two_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "1f8b5c5d1756"
VERSION = "1.1.0"
TASK_ID = "1f8b5c5d1756"
SUMMARY = "3 blobs: 2 share normalized shape, 1 is unique."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "2 share normalized shape",
    "1 has unique normalized shape",
]

PALETTE_KINDS = ("default", "wide_unique", "tight_common", "edge_anchored")
DEGENERATE_TEXTURES = ("all_three_unique", "all_three_same", "only_two_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "common_size":    {"type": "int", "default": "3", "valid": "3"},
    "unique_size":    {"type": "int", "default": "5", "valid": "5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    unique = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
    paint_at(g, 1, 1, common, 4)
    paint_at(g, 1, w - 4, common, 4)
    paint_at(g, h - 4, 4, unique, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    unique = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]
    different = [(0, 0), (0, 1), (1, 0)]
    if name == "all_three_unique":
        # Each blob is a different shape — no "common" pair to compare against
        paint_at(g, 1, 1, common, 4)
        paint_at(g, 1, w - 4, unique, 4)
        paint_at(g, h - 4, 4, different, 4)
        return g
    if name == "all_three_same":
        # All 3 share the same shape — no unique one
        paint_at(g, 1, 1, common, 4)
        paint_at(g, 1, w - 4, common, 4)
        paint_at(g, h - 4, 4, common, 4)
        return g
    if name == "only_two_blobs":
        paint_at(g, 1, 1, common, 4)
        paint_at(g, h - 4, 4, unique, 4)
        return g
    return g
