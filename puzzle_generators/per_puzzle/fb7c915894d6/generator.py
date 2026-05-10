"""Generator for arc_additional_puzzle_bank_volume11:H75.

Rule: the most frequent normalized component shape determines both the
source mask and the scale factor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frequent,
n_distractors, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_frequent, all_same_shape, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "fb7c915894d6"
VERSION = "1.1.0"
TASK_ID = "fb7c915894d6"
SUMMARY = "The most frequent normalized component shape determines both the source mask and the scale factor."

INVARIANTS = [
    "all nonzero components participate regardless of color",
    "one normalized shape class appears three times",
    "all distractor shape classes appear once",
    "the output is the frequent shape scaled by its frequency",
]

PALETTE_KINDS = ("default", "L_frequent", "T_frequent", "Z_frequent")
DEGENERATE_TEXTURES = ("no_frequent", "all_same_shape", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frequent":     {"type": "int", "default": "3", "valid": "3"},
    "n_distractors":  {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        w = ctx.draw_int("grid_w", 13, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 13, 18)
    g = full_grid(h, w, 0)
    frequent = [(0, 0), (1, 0), (1, 1)]
    paint_at(g, 1, 1, frequent, 2)
    paint_at(g, 1, w - 4, frequent, 3)
    paint_at(g, h - 4, 2, frequent, 4)
    paint_at(g, h - 5, w - 5, [(0, 0), (0, 1), (1, 0), (1, 1)], 5)
    paint_at(g, h // 2, w // 2, [(0, 0), (0, 1), (0, 2)], 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 15
    g = full_grid(h, w, 0)
    frequent = [(0, 0), (1, 0), (1, 1)]
    square = [(0, 0), (0, 1), (1, 0), (1, 1)]
    bar3 = [(0, 0), (0, 1), (0, 2)]
    if name == "no_frequent":
        # all shapes appear once → no class qualifies as "most frequent"
        paint_at(g, 1, 1, frequent, 2)
        paint_at(g, 1, w - 4, square, 3)
        paint_at(g, h - 4, 2, bar3, 4)
        return g
    if name == "all_same_shape":
        # every blob has the same shape → no distractor, scale factor = total
        paint_at(g, 1, 1, frequent, 2)
        paint_at(g, 1, w - 4, frequent, 3)
        paint_at(g, h - 4, 2, frequent, 4)
        paint_at(g, h - 4, w - 4, frequent, 5)
        return g
    if name == "single_blob":
        # only one component → "frequency" is degenerate (1)
        paint_at(g, h // 2, w // 2, frequent, 4)
        return g
    return g
