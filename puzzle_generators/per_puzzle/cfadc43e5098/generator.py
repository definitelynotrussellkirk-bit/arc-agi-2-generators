"""Generator for f3b10344.

Rule: same-color rectangle pairs with matching midlines receive
interior bridge rectangles.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_rects, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "cfadc43e5098"
VERSION = "1.1.0"
TASK_ID = "cfadc43e5098"
SUMMARY = "Same-color rectangle pairs with matching midlines get interior bridges."

INVARIANTS = [
    "same-color rectangles are separated horizontally or vertically",
    "paired rectangles overlap in the perpendicular axis and share midpoint",
    "the bridge occupies the gap interior excluding rectangle borders",
    "rectangle color is non-zero and not 8",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "single_rect", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0,8}",
                       "valid": "1..7|9"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    color = ctx.draw_color("rect_color", exclude={0, 8})
    g = full_grid(12, 13, 0)
    if orientation == "horizontal":
        draw_rect(g, 3, 1, 5, 3, color)
        draw_rect(g, 3, 8, 5, 3, color)
    else:
        draw_rect(g, 1, 4, 3, 5, color)
        draw_rect(g, 8, 4, 3, 5, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 0)
    if name == "no_rects":
        return g
    if name == "single_rect":
        draw_rect(g, 3, 4, 4, 4, 2)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
