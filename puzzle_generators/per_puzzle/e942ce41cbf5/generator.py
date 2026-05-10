"""Generator for arc_additional_puzzle_bank_volume21:H144.

Rule: operation control (3,4,6) and transform control (7,8,9) combine
a normalized blue mask with a transformed red mask.

Combinatorial axes (8): grid_h/w, palette_kind, op_control,
palette_size, position_bias, n_distinct_colors, transform_control, texture.
Degenerates: no_op_control, no_transform_control, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "e942ce41cbf5"
VERSION = "1.1.0"
TASK_ID = "e942ce41cbf5"
SUMMARY = "Operation and transform controls combine a normalized blue mask with a transformed red mask."

INVARIANTS = [
    "one operation control is 3, 4, or 6",
    "one transform control is 7, 8, or 9",
    "blue and red masks partially overlap after transformation",
    "the output is a cropped cyan mask",
]

PALETTE_KINDS = ("default", "op_3", "op_4", "op_6")
DEGENERATE_TEXTURES = ("no_op_control", "no_transform_control", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "op_control":     {"type": "int", "default": "rng 3|4|6",
                       "valid": "3|4|6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "transform_control": {"type": "int", "default": "rng 7|8|9",
                          "valid": "7|8|9"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 13, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[h - 1][0] = rng.choice([3, 4, 6])
    g[h - 1][w - 1] = rng.choice([7, 8, 9])
    blue = [(0, 0), (0, 1), (1, 1), (2, 1)]
    red = [(0, 0), (1, 0), (1, 1), (1, 2)]
    paint_at(g, 1, 1, blue, 1)
    paint_at(g, 1, 7, red, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    blue = [(0, 0), (0, 1), (1, 1), (2, 1)]
    red = [(0, 0), (1, 0), (1, 1), (1, 2)]
    if name == "no_op_control":
        # transform + blobs but no op → operation undefined
        g[h - 1][w - 1] = 7
        paint_at(g, 1, 1, blue, 1)
        paint_at(g, 1, 7, red, 2)
        return g
    if name == "no_transform_control":
        # op + blobs but no transform — red mask not transformed
        g[h - 1][0] = 4
        paint_at(g, 1, 1, blue, 1)
        paint_at(g, 1, 7, red, 2)
        return g
    if name == "no_blob":
        # both controls but no blue + red blobs to combine
        g[h - 1][0] = 6
        g[h - 1][w - 1] = 8
        return g
    return g
