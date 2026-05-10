"""Generator for arc_puzzle_bank_21_set10_e:medium_j08.

Rule: sort distinct perimeters desc; recolor each blob by perimeter
rank using palette [2 3 4 6 8 9 1 5 7].

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, perimeter_spread, texture.
Degenerates: tied_perimeters, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "2d6c272b0820"
VERSION = "1.1.0"
TASK_ID = "2d6c272b0820"
SUMMARY = "3 distinct-color blobs of varied perimeters."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "all distinct perimeters (so rank order is unambiguous)",
]

PALETTE_KINDS = ("default", "small_blobs", "mixed_blobs", "large_blobs")
DEGENERATE_TEXTURES = ("tied_perimeters", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "perimeter_spread": {"type": "str", "default": "8_10_12", "valid": "8_10_12"},
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
    paint_at(g, 1, 2, PLUS_5, 2)
    paint_at(g, 1, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
    paint_at(g, h - 3, 1, [(0, 0), (0, 1), (0, 2), (0, 3)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "tied_perimeters":
        # 3 blobs with the same perimeter → rank is ambiguous
        sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
        paint_at(g, 1, 1, sq, 2)
        paint_at(g, 1, w - 4, sq, 4)
        paint_at(g, h - 3, 1, sq, 7)
        return g
    if name == "single_blob":
        # only 1 blob → rule has nothing to rank against
        paint_at(g, 1, 2, PLUS_5, 2)
        return g
    if name == "no_blobs":
        # empty grid — no blobs at all
        return g
    return g
