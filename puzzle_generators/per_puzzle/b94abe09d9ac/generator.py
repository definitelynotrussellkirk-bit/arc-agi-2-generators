"""Generator for arc_additional_puzzles_21_set15_bundle:M103.

Rule: components sorted by c1; n×n matrix: 8 if shapes equal under
normalize, 0 else.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, shape_kind, texture.
Degenerates: all_match, all_distinct, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "b94abe09d9ac"
VERSION = "1.1.0"
TASK_ID = "b94abe09d9ac"
SUMMARY = "3 distinct-color blobs: 2 share normalized shape, 1 different."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "two share normalized shape",
    "one is different",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_match", "all_distinct", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "shape_kind":     {"type": "str", "default": "L_vs_T", "valid": "L_vs_T"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    common = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    different = [(0, 0), (0, 1), (0, 2), (1, 0)]
    paint_at(g, 1, 1, common, palette[0])
    paint_at(g, 1, 5, different, palette[1])
    paint_at(g, 1, 10, common, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 13
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    different = [(0, 0), (0, 1), (0, 2), (1, 0)]
    if name == "all_match":
        # all 3 blobs share a shape → matrix is uniformly 8 off-diagonal
        paint_at(g, 1, 1, common, 4)
        paint_at(g, 1, 5, common, 6)
        paint_at(g, 1, 10, common, 7)
        return g
    if name == "all_distinct":
        # all 3 blobs distinct → matrix has no 8s anywhere
        paint_at(g, 1, 1, common, 4)
        paint_at(g, 1, 5, different, 6)
        paint_at(g, 1, 10, [(0, 0), (0, 1), (1, 1), (2, 1)], 7)
        return g
    if name == "single_blob":
        # only one blob → matrix is 1×1 with 0 (no comparison possible)
        paint_at(g, 1, 5, common, 4)
        return g
    return g
