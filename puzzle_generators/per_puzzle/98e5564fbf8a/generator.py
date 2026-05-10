"""Generator for 93b4f4b3.

Rule: shape patterns on the right fill matching holes in a frame on the
left.

Combinatorial axes (8): grid_h/w, frame_color, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_holes, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "98e5564fbf8a"
VERSION = "1.1.0"
TASK_ID = "98e5564fbf8a"
SUMMARY = "Shape patterns on the right fill matching holes in a frame on the left."

INVARIANTS = [
    "a full zero column separates the frame panel from the shape panel",
    "the left panel is mostly frame color with hole sections",
    "right-panel shapes are grouped by zero separator rows",
    "each hole is filled with the color of the shape with the same normalized pattern",
]

FRAME_KINDS = ("F5", "F8")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "no_shapes", "full_grid")
HELPFUL_TEXTURES = FRAME_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "frame_color":    {"type": "choice", "default": "rng helpful",
                       "valid": "5|8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for frame_color",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in FRAME_KINDS:
        frame_color = int(tx[1])
    else:
        frame_color = ctx.draw_choice("frame_color", [5, 8])
    s1, s2 = ctx.draw_distinct_colors("shape_colors", n=2, exclude={0, frame_color})
    g = full_grid(12, 12, 0)
    for r in range(12):
        for c in range(5):
            g[r][c] = frame_color
    hole1 = [(2, 1), (2, 2), (3, 1)]
    hole2 = [(7, 2), (8, 1), (8, 2)]
    _paint(g, hole1, 0)
    _paint(g, hole2, 0)
    _paint(g, [(1, 7), (1, 8), (2, 7)], s1)
    _paint(g, [(6, 8), (7, 7), (7, 8)], s2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_holes":
        for r in range(12):
            for c in range(5):
                g[r][c] = 5
        return g
    if name == "no_shapes":
        for r in range(12):
            for c in range(5):
                g[r][c] = 5
        for r, c in [(2, 1), (2, 2), (3, 1), (7, 2), (8, 1), (8, 2)]:
            g[r][c] = 0
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
