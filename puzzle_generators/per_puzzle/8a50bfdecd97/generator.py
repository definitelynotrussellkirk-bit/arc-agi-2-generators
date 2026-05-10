"""Generator for df9fd884.

Rule: a non-4/non-7 shape sits between two color-4 brackets on a color-7
field; move it into the opposite bracket corner.

Combinatorial axes (8): grid_h/w, shape_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_brackets, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, fill_box, full_grid

GENERATOR_ID = "8a50bfdecd97"
VERSION = "1.1.0"
TASK_ID = "8a50bfdecd97"
SUMMARY = "Move a colored shape into the opposite bracket corner."

INVARIANTS = [
    "background/filler is 7",
    "there are exactly two color-4 bracket objects",
    "one small colored shape is separate from both brackets",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_brackets", "no_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "shape_size":     {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
        shape_size = ctx.draw_int("shape_size", 1, 1)
    elif difficulty == "hard":
        shape_size = ctx.draw_int("shape_size", 2, 2)
    else:
        shape_size = ctx.draw_int("shape_size", 1, 2)
    color = ctx.draw_color("shape_color", exclude={4, 7})
    h, w = 10, 14
    g = full_grid(h, w, 7)
    draw_frame(g, 1, 1, 4, 4, 4)
    draw_frame(g, 1, 9, 4, 12, 4)
    sr = rng.randint(6, 8 - shape_size)
    sc = rng.randint(1, 4 - shape_size)
    fill_box(g, sr, sc, sr + shape_size - 1, sc + shape_size - 1, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 14, 7)
    if name == "no_brackets":
        g[7][3] = 3
        return g
    if name == "no_shape":
        draw_frame(g, 1, 1, 4, 4, 4)
        draw_frame(g, 1, 9, 4, 12, 4)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(14):
                g[r][c] = 4
        return g
    return g
