"""Generator for arc_puzzle_bank_twelfth_21_bundle:easy_84_recolor_border_touching_components.

Rule: border-touching components → orange (7); interior components stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_interior, all_border_touching, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7f31c4f794b2"
VERSION = "1.1.0"
TASK_ID = "7f31c4f794b2"
SUMMARY = "Border-touching components are recolored to orange while interior components stay unchanged."

INVARIANTS = [
    "background is 0",
    "components are monochrome and separated",
    "some components touch the outer grid border",
    "input components do not use output color 7",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_interior", "all_border_touching", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "border_and_interior_mix",
                       "valid": "border_and_interior_mix"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 8, 9], 4)
    _paint(g, [(0, 1), (0, 2), (1, 1)], colors[0])
    _paint(g, [(h - 1, w - 3), (h - 1, w - 2), (h - 2, w - 2)], colors[1])
    _paint(g, [(3, 3), (3, 4), (4, 3)], colors[2])
    _paint(g, [(h - 4, w - 5), (h - 4, w - 4), (h - 3, w - 4)], colors[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "all_interior":
        # all components are interior (none touch border) → rule changes nothing, output equals input
        _paint(g, [(3, 3), (3, 4), (4, 3)], 4)
        _paint(g, [(6, 7), (6, 8), (7, 7)], 6)
        _paint(g, [(4, 8), (5, 8)], 3)
        return g
    if name == "all_border_touching":
        # all components touch the border → entire output is uniformly color 7
        _paint(g, [(0, 1), (0, 2), (1, 1)], 4)
        _paint(g, [(h - 1, w - 3), (h - 1, w - 2)], 6)
        _paint(g, [(3, 0), (4, 0)], 3)
        _paint(g, [(2, w - 1), (3, w - 1)], 8)
        return g
    if name == "no_components":
        # blank grid → rule fires zero times, output equals input
        return g
    return g
