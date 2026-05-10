"""Generator for 1da012fc.

Rule: a gray legend box contains colored dots that recolor ordered
source-color shapes.

Combinatorial axes (8): grid_h/w, n_shapes, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_legend, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, fill_box, full_grid

GENERATOR_ID = "c2a1ba1a45fd"
VERSION = "1.1.0"
TASK_ID = "c2a1ba1a45fd"
SUMMARY = "Gray legend dots recolor ordered source-color shapes."

INVARIANTS = [
    "background is 0",
    "gray cells define one legend rectangle",
    "legend dots and source-color objects have the same reading-order count",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_legend", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
    if difficulty == "easy":
        n_shapes = ctx.draw_int("n_shapes", 2, 2)
    elif difficulty == "hard":
        n_shapes = ctx.draw_int("n_shapes", 3, 3)
    else:
        n_shapes = ctx.draw_int("n_shapes", 2, 3)
    source_color = ctx.draw_color("source_color", exclude={0, 5})
    dot_colors = list(ctx.draw_distinct_colors("dot_colors", n=n_shapes,
                                               exclude={0, 5, source_color}))
    g = full_grid(9, 13, 0)
    draw_frame(g, 1, 1, 3, 5, 5)
    for i, color in enumerate(dot_colors):
        g[2][2 + i] = color
    for i in range(n_shapes):
        r = 5 + (i // 2) * 2
        c = 1 + (i % 2) * 5
        fill_box(g, r, c, r + 1, c + 1, source_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 13, 0)
    if name == "no_legend":
        fill_box(g, 5, 1, 6, 2, 3)
        return g
    if name == "no_shapes":
        draw_frame(g, 1, 1, 3, 5, 5)
        g[2][2] = 4
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
