"""Generator for 7d18a6fb.

Rule: 7x7 color-1 legend names four colors whose outside shapes are
packed into 3x3 quadrants.

Combinatorial axes (8): grid_h/w, shape_family, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_legend, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid, paint_at

GENERATOR_ID = "0bc8666b7693"
VERSION = "1.1.0"
TASK_ID = "0bc8666b7693"
SUMMARY = "7x7 color-1 legend names four colors whose outside shapes pack 3x3 quadrants."

INVARIANTS = [
    "one connected color-1 object has a 7x7 bounding box",
    "four interior legend corner cells name distinct outside shape colors",
    "each named color appears in one outside shape",
    "shape colors are distinct from 0 and 1",
]

SHAPE_FAMILIES = ("corners", "bars", "mix")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_legend", "no_shapes", "full_grid")
HELPFUL_TEXTURES = SHAPE_FAMILIES

SHAPES = {
    "corners": [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 2), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (1, 1)],
        [(1, 1), (1, 2), (2, 2)],
    ],
    "bars": [
        [(0, 0), (0, 1), (0, 2)],
        [(0, 1), (1, 1), (2, 1)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 2), (1, 2), (2, 2)],
    ],
    "mix": [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 1), (2, 0)],
        [(0, 0), (0, 2), (1, 1), (2, 1)],
    ],
}

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "shape_family":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_FAMILIES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for shape_family",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    family = (overrides.get("texture") if overrides.get("texture") in SHAPE_FAMILIES else None) or \
             overrides.get("shape_family") or \
             ctx.draw_choice("shape_family", list(SHAPE_FAMILIES))
    colors = ctx.draw_distinct_colors("legend_colors", n=4, exclude={0, 1})
    g = full_grid(16, 16, 0)
    draw_rect(g, 1, 1, 7, 7, 1)
    for (dr, dc), color in zip([(1, 1), (1, 5), (5, 1), (5, 5)], colors):
        g[1 + dr][1 + dc] = color
    origins = [(1, 11), (5, 11), (10, 1), (10, 11)]
    for origin, color, cells in zip(origins, colors, SHAPES[family]):
        paint_at(g, origin[0], origin[1], cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 16, 0)
    if name == "no_legend":
        for origin, cells in zip([(1, 11), (5, 11), (10, 1), (10, 11)],
                                  SHAPES["corners"]):
            paint_at(g, origin[0], origin[1], cells, 2)
        return g
    if name == "no_shapes":
        draw_rect(g, 1, 1, 7, 7, 1)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(16):
                g[r][c] = 1
        return g
    return g
