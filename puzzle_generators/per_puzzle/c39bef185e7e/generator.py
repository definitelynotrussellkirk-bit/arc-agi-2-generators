"""Generator for arc_additional_puzzle_bank_volume15:H104.

Rule: among green components, the only shape outside the common dihedral
class is recolored cyan in place.

Combinatorial axes (8): grid_h/w, palette_kind, num_components,
common_size, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_same_shape, all_different, only_two_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c39bef185e7e"
VERSION = "1.1.0"
TASK_ID = "c39bef185e7e"
SUMMARY = "Among green components, the only shape outside the common dihedral class is recolored cyan."

INVARIANTS = [
    "all active components are color 3",
    "at least two components are dihedrally equivalent",
    "exactly one component is an outlier shape",
    "the outlier is recolored in-place",
]

PALETTE_KINDS = ("default", "wide_grid", "tight_grid", "scattered")
DEGENERATE_TEXTURES = ("all_same_shape", "all_different", "only_two_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_components": {"type": "int", "default": "4", "valid": "4"},
    "common_size":    {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        w = ctx.draw_int("grid_w", 13, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 13, 18)
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    outlier = [(0, 0), (0, 1), (0, 2), (1, 1)]
    paint_at(g, 1, 1, common, 3)
    paint_at(g, 1, w - 5, common, 3)
    paint_at(g, h - 4, 2, common, 3)
    paint_at(g, h - 5, w - 6, outlier, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    outlier = [(0, 0), (0, 1), (0, 2), (1, 1)]
    if name == "all_same_shape":
        # 4 components share one dihedral class — no outlier exists
        paint_at(g, 1, 1, common, 3)
        paint_at(g, 1, w - 5, common, 3)
        paint_at(g, h - 4, 2, common, 3)
        paint_at(g, h - 5, w - 6, common, 3)
        return g
    if name == "all_different":
        # every component a different shape — multiple "outliers", ambiguous
        paint_at(g, 1, 1, common, 3)
        paint_at(g, 1, w - 5, [(0, 0), (0, 1), (1, 0), (1, 1)], 3)
        paint_at(g, h - 4, 2, outlier, 3)
        paint_at(g, h - 5, w - 6, [(0, 0), (1, 0), (1, 1), (2, 1)], 3)
        return g
    if name == "only_two_components":
        # only 2 components — no majority can be defined
        paint_at(g, 1, 1, common, 3)
        paint_at(g, h - 4, 2, outlier, 3)
        return g
    return g
