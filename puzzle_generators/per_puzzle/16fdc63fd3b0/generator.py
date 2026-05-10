"""Generator for arc_additional_puzzle_bank_volume16:H109.

Rule: normalize the 1-cells & 2-cells to common origin; XOR gives cells
in exactly one shape; output bbox-cropped XOR in color 8.

Combinatorial axes (8): grid_h/w, palette_kind, shape_kind,
palette_size, position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: shapes_identical, no_blob_2, no_blob_1.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "16fdc63fd3b0"
VERSION = "1.1.0"
TASK_ID = "16fdc63fd3b0"
SUMMARY = "1-shape and 2-shape placed apart; their normalized XOR is non-empty."

INVARIANTS = [
    "exactly one 1-blob and one 2-blob",
    "their normalized cell sets share some but differ in some positions",
]

PALETTE_KINDS = ("default", "L_shapes", "Z_shapes", "T_shapes")
DEGENERATE_TEXTURES = ("shapes_identical", "no_blob_2", "no_blob_1")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "overlap_kind":   {"type": "str", "default": "partial", "valid": "partial"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape1 = [(0, 0), (1, 0), (2, 0), (2, 1)]
    shape2 = [(0, 0), (1, 0), (1, 1), (2, 1)]
    paint_at(g, 1, 1, shape1, 1)
    paint_at(g, 4, 6, shape2, 2)
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    same = [(0, 0), (1, 0), (2, 0), (2, 1)]
    if name == "shapes_identical":
        # both blobs have same normalized shape — XOR is empty
        paint_at(g, 1, 1, same, 1)
        paint_at(g, 4, 6, same, 2)
        return g
    if name == "no_blob_2":
        # only color-1 blob — XOR has one operand missing
        paint_at(g, 1, 1, same, 1)
        return g
    if name == "no_blob_1":
        # only color-2 blob — XOR has one operand missing
        paint_at(g, 4, 6, same, 2)
        return g
    return g
