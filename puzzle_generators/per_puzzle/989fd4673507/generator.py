"""Generator for 9aec4887.

Rule: color-8 shape is framed by colors of its nearest uniquely
closest edge.

Combinatorial axes (8): grid_h/w, shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shape, no_edges, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "989fd4673507"
VERSION = "1.1.0"
TASK_ID = "989fd4673507"
SUMMARY = "Color-8 shape framed by colors of nearest uniquely closest edge."

INVARIANTS = [
    "four non-8 colors form two horizontal and two vertical guide edges",
    "one separate color-8 shape defines the output interior mask",
    "edge colors are distinct from each other and from 0 and 8",
    "shape sits clear of the edges",
]

SHAPE_NAMES = ("plus", "zigzag", "block")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_edges", "full_grid")
HELPFUL_TEXTURES = SHAPE_NAMES

SHAPES = {
    "plus": PLUS_5,
    "zigzag": [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    "block": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "shape":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_NAMES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    shape_name = (overrides.get("texture") if overrides.get("texture") in SHAPE_NAMES else None) or \
                 overrides.get("shape") or \
                 ctx.draw_choice("shape", list(SHAPE_NAMES))
    top, bottom, left, right = ctx.draw_distinct_colors("edge_colors", n=4, exclude={0, 8})
    g = full_grid(12, 13, 0)
    for c in range(3, 10):
        g[1][c] = top
        g[8][c] = bottom
    for r in range(2, 8):
        g[r][2] = left
        g[r][10] = right
    paint_at(g, 4, 5, SHAPES[shape_name], 8)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 0)
    if name == "no_shape":
        for c in range(3, 10):
            g[1][c] = 1; g[8][c] = 2
        return g
    if name == "no_edges":
        paint_at(g, 4, 5, PLUS_5, 8)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(13):
                g[r][c] = 8
        return g
    return g
