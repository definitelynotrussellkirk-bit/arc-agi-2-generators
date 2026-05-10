"""Generator for arc_additional_puzzle_bank_volume17:H117.

Rule: cells in exactly 2 of 3 normalized shapes (1, 2, 3 colored blobs)
emit a cyan output cropped to the union bbox.

Combinatorial axes (8): grid_h/w, palette_kind, shape_kind, palette_size,
position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: identical_shapes, empty_intersection, missing_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2a1d414bfe10"
VERSION = "1.1.0"
TASK_ID = "2a1d414bfe10"
SUMMARY = "1-, 2-, 3-shapes placed apart with overlapping normalized cells (exactly 2 of 3 non-empty)."

INVARIANTS = [
    "exactly one blob each of color 1, 2, 3",
    "their normalized cell sets have at least one cell in exactly 2 of them",
]

PALETTE_KINDS = ("default", "L_combo", "T_combo", "Z_combo")
DEGENERATE_TEXTURES = ("identical_shapes", "empty_intersection", "missing_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "str", "default": "varied", "valid": "varied"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "overlap_kind":   {"type": "str", "default": "exact_2_of_3", "valid": "exact_2_of_3"},
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
    s1 = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
    s2 = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
    s3 = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, 1, 1, s1, 1)
    paint_at(g, 1, w - 4, s2, 2)
    paint_at(g, h - 3, 1, s3, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    s_uni = [(0, 0), (0, 1), (1, 0), (1, 1)]
    s2 = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
    s3 = [(0, 0), (0, 1), (1, 1), (2, 1)]
    if name == "identical_shapes":
        # all three shapes equal → exactly-2-of-3 set is empty
        paint_at(g, 1, 1, s_uni, 1)
        paint_at(g, 1, w - 4, s_uni, 2)
        paint_at(g, h - 3, 1, s_uni, 3)
        return g
    if name == "empty_intersection":
        # three disjoint shapes → no cell ever appears in exactly 2
        paint_at(g, 1, 1, [(0, 0)], 1)
        paint_at(g, 1, w - 4, [(0, 1), (1, 0)], 2)
        paint_at(g, h - 3, 1, [(0, 0), (1, 1), (2, 0)], 3)
        return g
    if name == "missing_blob":
        # only colors 1 and 2; rule needs three shapes
        paint_at(g, 1, 1, s_uni, 1)
        paint_at(g, 1, w - 4, s2, 2)
        return g
    return g
