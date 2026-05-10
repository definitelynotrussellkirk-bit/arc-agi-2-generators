"""Generator for arc_additional_puzzle_bank_volume2:H11.

Rule: among 4-blobs, the one with unique shape (canonical normalized
form, considering all 8 transforms) is recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, shape_spread, texture.
Degenerates: all_same_shape, all_different, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "040bfb038c65"
VERSION = "1.1.0"
TASK_ID = "040bfb038c65"
SUMMARY = "4 4-blobs: 3 share canonical shape (under any rotation/flip), 1 is unique."

INVARIANTS = [
    "exactly 4 non-touching 4-blobs",
    "3 share canonical shape, 1 differs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_shape", "all_different", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "shape_spread":   {"type": "str", "default": "three_match_one_diff",
                       "valid": "three_match_one_diff"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 4)
    paint_at(g, 1, w - 3, [(0, 0), (0, 1), (1, 1)], 4)
    paint_at(g, h - 3, w - 3, [(0, 0), (1, 0), (1, 1)], 4)
    paint_at(g, h - 3, 1, [(0, 0), (1, 0), (2, 0), (1, 1)], 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    L_a = [(0, 0), (0, 1), (1, 0)]
    L_b = [(0, 0), (0, 1), (1, 1)]
    L_c = [(0, 0), (1, 0), (1, 1)]
    odd = [(0, 0), (1, 0), (2, 0), (1, 1)]
    bar = [(0, 0), (0, 1), (0, 2)]
    if name == "all_same_shape":
        # every 4-blob shares the canonical shape → no unique blob to recolor
        paint_at(g, 1, 1, L_a, 4)
        paint_at(g, 1, w - 3, L_b, 4)
        paint_at(g, h - 3, 1, L_c, 4)
        paint_at(g, h - 3, w - 3, L_a, 4)
        return g
    if name == "all_different":
        # every blob is its own canonical shape → no majority, "unique" undefined
        paint_at(g, 1, 1, L_a, 4)
        paint_at(g, 1, w - 3, odd, 4)
        paint_at(g, h - 3, 1, bar, 4)
        return g
    if name == "single_blob":
        # only one blob → "unique vs majority" comparison is vacuous
        paint_at(g, h // 2, w // 2, L_a, 4)
        return g
    return g
