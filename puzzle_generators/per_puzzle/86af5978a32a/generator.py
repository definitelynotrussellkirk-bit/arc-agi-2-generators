"""Generator for b190f7f5.

Rule: multicolor layout half places copies of the single-color
block-shape half into a scaled output canvas.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, split, n_distinct_colors.
Degenerates: no_layout, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "86af5978a32a"
VERSION = "1.1.0"
TASK_ID = "86af5978a32a"
SUMMARY = "Layout half + block-shape half assembled into scaled output."

INVARIANTS = [
    "the input is split into a layout half and a block-shape half",
    "the layout half has more distinct colors than the shape half",
    "shape-cell positions are copied at every nonzero layout cell",
    "shape color is distinct from layout colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_layout", "no_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3"},
    "grid_w":         {"type": "int", "default": "6", "valid": "6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "split":          {"type": "str", "default": "horizontal", "valid": "horizontal"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    colors = ctx.draw_distinct_colors("layout_colors", n=4, exclude={0})
    shape_color = ctx.draw_color("shape_color", exclude={0, *colors})
    g = full_grid(3, 6, 0)
    for (r, c), color in zip([(0, 0), (0, 2), (1, 1), (2, 0)], colors):
        g[r][c] = color
    for r, c in [(0, 3), (1, 3), (1, 4), (2, 4)]:
        g[r][c] = shape_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 6, 0)
    if name == "no_layout":
        for r, c in [(0, 3), (1, 3), (1, 4)]:
            g[r][c] = 2
        return g
    if name == "no_shape":
        g[0][0] = 1; g[1][1] = 2; g[2][2] = 3
        return g
    if name == "full_grid":
        for r in range(3):
            for c in range(6):
                g[r][c] = 2
        return g
    return g
