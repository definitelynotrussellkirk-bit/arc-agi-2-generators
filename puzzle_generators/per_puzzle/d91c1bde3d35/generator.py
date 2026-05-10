"""Generator for arc_additional_puzzles_21_set14_bundle:H97.

Rule: sort objects by (r1, c1); n×n matrix with 8 if normalized cells
equal, 0 else.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, shape_spread, texture.
Degenerates: all_same_shape, all_different, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d91c1bde3d35"
VERSION = "1.1.0"
TASK_ID = "d91c1bde3d35"
SUMMARY = "3 distinct-color blobs: two share normalized shape, one differs."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "two share their normalized shape, one is different",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_shape", "all_different", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "shape_spread":   {"type": "str", "default": "two_match_one_diff",
                       "valid": "two_match_one_diff"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    shape_a = [(0, 0), (1, 0), (2, 0)]
    shape_b = [(0, 0), (0, 1), (0, 2), (1, 1)]
    paint_at(g, 1, 1, shape_a, palette[0])
    paint_at(g, 1, w - 4, shape_a, palette[1])
    paint_at(g, h - 3, w // 2 - 2, shape_b, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    shape_a = [(0, 0), (1, 0), (2, 0)]
    shape_b = [(0, 0), (0, 1), (0, 2), (1, 1)]
    shape_c = [(0, 0), (0, 1), (1, 0), (1, 1)]
    if name == "all_same_shape":
        # every object normalizes to the same shape → matrix is all-8
        paint_at(g, 1, 1, shape_a, 2)
        paint_at(g, 1, w - 4, shape_a, 3)
        paint_at(g, h - 4, w // 2 - 1, shape_a, 4)
        return g
    if name == "all_different":
        # every object has a unique shape → matrix is identity (only diag is 8)
        paint_at(g, 1, 1, shape_a, 2)
        paint_at(g, 1, w - 4, shape_b, 3)
        paint_at(g, h - 3, w // 2 - 2, shape_c, 4)
        return g
    if name == "single_object":
        # only one object → the matrix degenerates to a 1×1 trivial case
        paint_at(g, h // 2, w // 2, shape_a, 5)
        return g
    return g
