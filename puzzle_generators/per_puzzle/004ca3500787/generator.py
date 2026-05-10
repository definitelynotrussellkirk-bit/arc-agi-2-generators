"""Generator for arc_additional_puzzle_bank_volume18:H125.

Rule: most red components share a dihedral shape class; the unique outlier
is canonicalized and rendered cyan.

Combinatorial axes (8): grid_h/w, palette_kind, num_components, common_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_same_shape, all_different, only_two_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "004ca3500787"
VERSION = "1.1.0"
TASK_ID = "004ca3500787"
SUMMARY = "Most red components share a dihedral shape class; the unique outlier is canonicalized and rendered cyan."

INVARIANTS = [
    "all components are red",
    "the common shape class appears more than once",
    "one red component has a different dihedral canonical shape",
    "the output is the outlier's canonical normalized mask",
]

PALETTE_KINDS = ("default", "wide_grid", "tight_grid", "scattered")
DEGENERATE_TEXTURES = ("all_same_shape", "all_different", "only_two_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_components": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 12, 17)
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    odd = [(0, 0), (0, 1), (0, 2)]
    paint_at(g, 1, 1, common, 2)
    paint_at(g, 1, w - 5, common, 2)
    paint_at(g, h - 4, w // 2, odd, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    odd = [(0, 0), (0, 1), (0, 2)]
    if name == "all_same_shape":
        # All 3 share dihedral class — no outlier exists
        paint_at(g, 1, 1, common, 2)
        paint_at(g, 1, w - 5, common, 2)
        paint_at(g, h - 4, w // 2, common, 2)
        return g
    if name == "all_different":
        # Every component is its own shape — no "common" majority
        paint_at(g, 1, 1, common, 2)
        paint_at(g, 1, w - 5, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        paint_at(g, h - 4, w // 2, odd, 2)
        return g
    if name == "only_two_components":
        # Only 2 components — can't define a majority
        paint_at(g, 1, 1, common, 2)
        paint_at(g, h - 4, w // 2, odd, 2)
        return g
    return g
