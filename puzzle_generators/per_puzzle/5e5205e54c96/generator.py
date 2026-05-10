"""Generator for arc_additional_puzzles_21_set9:H59.

Rule: nested 8-frame rings get filled (outer-to-inner) using the colors
listed in the top row of the legend.

Combinatorial axes (8): grid_h/w, palette_kind, depth, palette_size,
position_bias, n_distinct_colors, legend_order, texture.
Degenerates: no_legend, only_one_frame, frames_collide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5e5205e54c96"
VERSION = "1.1.0"
TASK_ID = "5e5205e54c96"
SUMMARY = "Fill nested color-8 frame rings from the top-row outer-to-inner legend."

INVARIANTS = [
    "top-row nonzero cells are the outer-to-inner ring colors",
    "all nested frames are color 8 and below the legend row",
    "nested frames are separated by zero space so each is a distinct component",
    "the deepest legend color fills the innermost open region",
]

PALETTE_KINDS = ("default", "warm_legend", "cool_legend", "rainbow")
DEGENERATE_TEXTURES = ("no_legend", "only_one_frame", "frames_collide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "depth":          {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "centered", "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4",
                          "valid": "3..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BOXES = [
    (2, 2, 14, 14),
    (5, 5, 11, 11),
    (7, 7, 9, 9),
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        depth = ctx.draw_int("depth", 2, 2)
    elif difficulty == "hard":
        depth = ctx.draw_int("depth", 3, 3)
    else:
        depth = ctx.draw_int("depth", 2, 3)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], depth)
    g = full_grid(15, 15, 0)
    for c, color in enumerate(colors):
        g[0][c] = color
    for box in _BOXES[:depth]:
        draw_frame(g, *box, 8)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_legend":
        for box in _BOXES[:2]:
            draw_frame(g, *box, 8)
        return g
    if name == "only_one_frame":
        g[0][0] = 3
        draw_frame(g, *_BOXES[0], 8)
        return g
    if name == "frames_collide":
        g[0][0] = 3
        g[0][1] = 4
        draw_frame(g, 2, 2, 14, 14, 8)
        draw_frame(g, 3, 3, 13, 13, 8)
        return g
    return g
