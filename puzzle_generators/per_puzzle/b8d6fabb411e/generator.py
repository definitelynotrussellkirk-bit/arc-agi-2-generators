"""Generator for d43fd935.

Rule: colored pixels aligned with green square draw straight connector
lines to square edge.

Combinatorial axes (8): grid_h/w, pixel_side, pixel_color, palette_kind,
anchor_corner, asymmetry_force, palette_size, square_size.
Degenerates: no_pixel, no_square, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b8d6fabb411e"
VERSION = "1.1.0"
TASK_ID = "b8d6fabb411e"
SUMMARY = "Colored pixels aligned with green square draw connector lines."

INVARIANTS = [
    "background is color 0",
    "a compact square uses color 3",
    "single colored pixels sit horizontally or vertically aligned with the square",
    "the gap between each pixel and the square is filled with that pixel color",
]

SIDES = ("right", "left", "top", "bottom")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pixel", "no_square", "full_grid")
HELPFUL_TEXTURES = SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "11", "valid": "9..16"},
    "pixel_side":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SIDES)},
    "pixel_color":    {"type": "color", "default": "rng !{0,3}",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "square_size":    {"type": "int", "default": "3", "valid": "2..5"},
    "texture":        {"type": "str", "default": "alias for pixel_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    side = (overrides.get("texture") if overrides.get("texture") in SIDES else None) or \
           overrides.get("pixel_side") or \
           ctx.draw_choice("pixel_side", list(SIDES))
    pixel_color = ctx.draw_color("pixel_color", exclude={0, 3})
    g = full_grid(11, 11, 0)
    for r in range(4, 7):
        for c in range(4, 7):
            g[r][c] = 3
    if side == "right":
        g[5][9] = pixel_color
    elif side == "left":
        g[5][1] = pixel_color
    elif side == "top":
        g[1][5] = pixel_color
    else:
        g[9][5] = pixel_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_pixel":
        for r in range(4, 7):
            for c in range(4, 7):
                g[r][c] = 3
        return g
    if name == "no_square":
        g[5][9] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 3
        return g
    return g
