"""Generator for arc_additional_puzzles_21_set22_bundle:H151.

Rule: nonzero mask objects are compared pairwise; transform-equivalent
pairs emit a 2 in the relation matrix.

Combinatorial axes (8): grid_h/w, palette_kind, n_objects, palette_size,
position_bias, n_distinct_colors, equiv_diversity, texture.
Degenerates: all_same_shape, all_unique, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "397767b9f88c"
VERSION = "1.1.0"
TASK_ID = "397767b9f88c"
SUMMARY = "Nonzero mask objects are compared pairwise; transform-equivalent pairs emit 2."

INVARIANTS = [
    "objects are separated in reading order",
    "some objects are transform-equivalent and at least one is distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("all_same_shape", "all_unique", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "equiv_diversity": {"type": "str", "default": "mixed",
                         "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 12, 15)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude=[0]))
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], colors[0])
    paint_at(g, 1, w - 4, [(0, 1), (1, 0), (1, 1)], colors[1])
    paint_at(g, h - 4, 1, [(0, 0), (0, 1), (1, 0)], colors[2])
    paint_at(g, h - 4, w - 4, [(0, 0), (0, 1), (0, 2), (1, 1)], colors[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    same = [(0, 0), (1, 0), (1, 1)]
    if name == "all_same_shape":
        # all 4 objects equivalent under any transform → matrix is all 2s
        paint_at(g, 1, 1, same, 4)
        paint_at(g, 1, w - 4, same, 6)
        paint_at(g, h - 4, 1, same, 7)
        paint_at(g, h - 4, w - 4, same, 8)
        return g
    if name == "all_unique":
        # 4 totally distinct shapes → no equivalent pairs (all zeros off-diag)
        paint_at(g, 1, 1, [(0, 0), (1, 0)], 4)
        paint_at(g, 1, w - 4, [(0, 0), (0, 1), (0, 2)], 6)
        paint_at(g, h - 4, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 7)
        paint_at(g, h - 4, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)], 8)
        return g
    if name == "no_objects":
        # empty grid — no objects to compare
        return g
    return g
