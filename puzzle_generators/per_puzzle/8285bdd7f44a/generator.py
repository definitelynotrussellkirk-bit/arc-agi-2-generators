"""Generator for arc_puzzle_bank_21_set14_s:S14_M3 — crop unique odd row-profile object.

Rule: two objects share a row profile and the unique odd row-profile
object is cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, odd_side,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_same_profile, all_distinct_profiles, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "8285bdd7f44a"
VERSION = "1.1.0"
TASK_ID = "8285bdd7f44a"
SUMMARY = "Two objects share a row profile and the unique odd row-profile object is cropped."

INVARIANTS = [
    "background is 0",
    "exactly two objects share the same row-count profile",
    "exactly one object has a unique row-count profile",
    "objects are separated from one another",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_profile", "all_distinct_profiles", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..12", "valid": "9..15"},
    "width":          {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "odd_side":       {"type": "enum", "default": "rng left|right",
                       "valid": "left|right"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_common_one_odd_profiles",
                       "valid": "two_common_one_odd_profiles"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

COMMON = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
ODD = [(0, 0), (0, 1), (1, 1), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 15, 16)
    else:
        h = ctx.draw_int("height", 10, 12)
        w = ctx.draw_int("width", 13, 16)
    odd_side = ctx.draw_choice("odd_side", ["left", "right"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r0 = rng.randint(1, 2)
    if odd_side == "left":
        paint_at(g, r0, 1, ODD, 2)
        paint_at(g, r0, 6, COMMON, 3)
        paint_at(g, h - 4, w - 5, COMMON, 4)
    else:
        paint_at(g, r0, 1, COMMON, 3)
        paint_at(g, r0, 6, COMMON, 4)
        paint_at(g, h - 4, w - 4, ODD, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "all_same_profile":
        # all 3 objects share same row-count profile → no unique odd one
        paint_at(g, 1, 1, COMMON, 2)
        paint_at(g, 1, 6, COMMON, 3)
        paint_at(g, h - 4, 1, COMMON, 4)
        return g
    if name == "all_distinct_profiles":
        # all 3 distinct profiles → no two share, no "shared" majority either
        paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2)], 2)        # row count [3]
        paint_at(g, 1, 6, ODD, 3)                              # row count [2,1,1]
        paint_at(g, h - 4, 1, COMMON, 4)                       # row count [1,3,1]
        return g
    if name == "single_object":
        # only 1 object → "shared profile" requires ≥2, precondition fails
        paint_at(g, 4, 5, COMMON, 2)
        return g
    return g
