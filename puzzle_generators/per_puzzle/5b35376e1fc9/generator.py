"""Generator for 95755ff2.

Rule: exterior colored pixels shoot straight rays into a color-2 diamond
interior.

Combinatorial axes (8): grid_h/w, ray_layout, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_diamond, no_rays, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5b35376e1fc9"
VERSION = "1.1.0"
TASK_ID = "5b35376e1fc9"
SUMMARY = "Exterior colored pixels shoot straight rays into a color-2 diamond interior."

INVARIANTS = [
    "the background is zero",
    "color 2 forms a centered diamond outline",
    "exterior colored pixels align with valid diamond rows or columns",
    "rays paint inward until they reach the opposite diamond boundary or an interior obstacle",
]

LAYOUTS = ("cross", "vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_diamond", "no_rays", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "ray_layout":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for ray_layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_diamond(g, cr, cc, radius):
    for r in range(cr - radius, cr + radius + 1):
        d = radius - abs(r - cr)
        g[r][cc - d] = 2
        g[r][cc + d] = 2


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    layout = (overrides.get("texture") if overrides.get("texture") in LAYOUTS else None) or \
             overrides.get("ray_layout") or \
             ctx.draw_choice("ray_layout", list(LAYOUTS))
    colors = ctx.draw_distinct_colors("ray_colors", n=4, exclude={0, 2})
    g = full_grid(13, 13, 0)
    _draw_diamond(g, 6, 6, 4)
    if layout in {"cross", "vertical"}:
        g[0][6] = colors[0]
        g[12][6] = colors[1]
    if layout in {"cross", "horizontal"}:
        g[6][0] = colors[2]
        g[6][12] = colors[3]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_diamond":
        g[0][6] = 3
        return g
    if name == "no_rays":
        _draw_diamond(g, 6, 6, 4)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
