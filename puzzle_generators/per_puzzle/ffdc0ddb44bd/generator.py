"""Generator for arc_puzzle_bank_21_set15:S15_M6 — most-frequent normalized shape.

Rule: among candidate objects, find the most-frequent normalized shape;
crop and recolor it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, majority_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_counts, single_object, all_distinct_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ffdc0ddb44bd"
VERSION = "1.1.0"
TASK_ID = "ffdc0ddb44bd"
SUMMARY = "The most frequent normalized candidate shape is cropped and recolored."

INVARIANTS = [
    "background is 0",
    "candidate objects use colors 2 through 6",
    "one normalized shape appears strictly more often than every other candidate shape",
    "candidate objects are separated from one another",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_counts", "single_object", "all_distinct_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "width":          {"type": "int", "default": "rng 16..19", "valid": "14..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "majority_count": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "majority_shape_with_decoys",
                       "valid": "majority_shape_with_decoys"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

MAJORITY = [(0, 0), (1, 0), (1, 1), (2, 1)]
ODD_A = [(0, 0), (0, 1), (1, 1)]
ODD_B = [(0, 1), (1, 0), (1, 1), (1, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 16, 17)
        majority_count = ctx.draw_int("majority_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 14, 15)
        w = ctx.draw_int("width", 18, 19)
        majority_count = ctx.draw_int("majority_count", 4, 4)
    else:
        h = ctx.draw_int("height", 12, 15)
        w = ctx.draw_int("width", 16, 19)
        majority_count = ctx.draw_int("majority_count", 3, 4)
    g = full_grid(h, w, 0)

    anchors = [(1, 1), (1, 6), (h - 5, 1), (h - 5, 6)]
    for color, (r, c) in zip(range(2, 2 + majority_count), anchors):
        paint_at(g, r, c, MAJORITY, color)
    paint_at(g, 1, w - 5, ODD_A, 6)
    if majority_count < 4:
        paint_at(g, h - 4, w - 5, ODD_B, 5)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 17
    g = full_grid(h, w, 0)
    if name == "tied_counts":
        # 2 distinct shapes each appearing 2 times → "most frequent" is tied
        paint_at(g, 1, 1, MAJORITY, 2)
        paint_at(g, 1, 6, MAJORITY, 3)
        paint_at(g, h - 4, 1, ODD_A, 4)
        paint_at(g, h - 4, 6, ODD_A, 5)
        return g
    if name == "single_object":
        # only 1 candidate → "most frequent" trivially that one
        paint_at(g, 4, 4, MAJORITY, 2)
        return g
    if name == "all_distinct_shapes":
        # all candidates have distinct shapes → no shape has count > 1
        paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2)], 2)            # line
        paint_at(g, 1, 6, MAJORITY, 3)                              # S
        paint_at(g, h - 5, 1, ODD_A, 4)                             # corner
        paint_at(g, h - 5, 6, ODD_B, 5)                             # T
        return g
    return g
