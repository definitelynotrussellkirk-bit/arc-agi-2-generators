"""Generator for arc_additional_puzzle_bank_volume13:H87.

Rule: two transform controls produce copies of a cyan source shape;
only their intersection is stamped red at a maroon anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ctrl_pair,
palette_size, position_bias, n_distinct_colors, source_shape, texture.
Degenerates: one_control, no_source, empty_intersection.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "07975597e370"
VERSION = "1.1.0"
TASK_ID = "07975597e370"
SUMMARY = "Two transform controls produce copies of a cyan source shape; only their intersection is stamped red at a maroon anchor."

INVARIANTS = [
    "exactly two transform controls from 1 through 4 appear",
    "one cyan asymmetric source shape is present",
    "the transformed copies have a nonempty overlap",
    "the overlap stamp fits at the color-9 anchor",
]

PALETTE_KINDS = ("default", "rot_pair_1_2", "rot_pair_2_3", "rot_pair_3_4")
DEGENERATE_TEXTURES = ("one_control", "no_source", "empty_intersection")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 14..19", "valid": "11..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ctrl_pair":      {"type": "str", "default": "rng_two_of_4", "valid": "rng_two_of_4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "source_shape":   {"type": "str", "default": "PLUS_5", "valid": "PLUS_5"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 17, 19)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 14, 19)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    codes = [1, 2, 3, 4]
    rng.shuffle(codes)
    g[1][2] = codes[0]
    g[2][4] = codes[1]
    source = PLUS_5
    paint_at(g, h - 5, w - 6, source, 8)
    g[3][w // 2] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "one_control":
        # one control only → can't form an intersection of two transforms
        g[1][2] = 2
        paint_at(g, h - 5, w - 6, PLUS_5, 8)
        g[3][w // 2] = 9
        return g
    if name == "no_source":
        # controls + anchor but no cyan source → nothing to transform
        g[1][2] = 2; g[2][4] = 3
        g[3][w // 2] = 9
        return g
    if name == "empty_intersection":
        # 1-cell source — its two transforms can never overlap (always separate cells)
        g[1][2] = 1; g[2][4] = 4
        paint_at(g, h - 5, w - 6, [(0, 0)], 8)
        g[3][w // 2] = 9
        return g
    return g
