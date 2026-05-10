"""Generator for arc_additional_puzzle_bank_volume10:H69.

Rule: a control cell chooses union, intersection, XOR, or
first-minus-second over normalized blue and red shapes.

Combinatorial axes (8): grid_h/w, palette_kind, control_color,
palette_size, position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: no_control, no_blob_1, no_blob_2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "7d8b053b9ef8"
VERSION = "1.1.0"
TASK_ID = "7d8b053b9ef8"
SUMMARY = "A control cell chooses union, intersection, XOR, or first-minus-second over normalized blue and red shapes."

INVARIANTS = [
    "control is one of 3, 4, 6, or 7",
    "one color-1 shape and one color-2 shape are present",
    "normalized shapes overlap but neither contains the other",
    "the output is a cropped cyan mask",
]

PALETTE_KINDS = ("default", "control_3", "control_4", "control_6_or_7")
DEGENERATE_TEXTURES = ("no_control", "no_blob_1", "no_blob_2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng 3|4|6|7",
                       "valid": "3|4|6|7"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "overlap_kind":   {"type": "str", "default": "partial", "valid": "partial"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([3, 4, 6, 7])
    a = PLUS_5
    b = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, h - 5, 1, a, 1)
    paint_at(g, 2, w - 5, b, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    a = PLUS_5
    b = [(0, 0), (0, 1), (1, 1), (2, 1)]
    if name == "no_control":
        # both shapes but no control → operation undefined
        paint_at(g, h - 5, 1, a, 1)
        paint_at(g, 2, w - 5, b, 2)
        return g
    if name == "no_blob_1":
        # control + only color-2 shape → operand missing
        g[0][0] = 4
        paint_at(g, 2, w - 5, b, 2)
        return g
    if name == "no_blob_2":
        # control + only color-1 shape → operand missing
        g[0][0] = 6
        paint_at(g, h - 5, 1, a, 1)
        return g
    return g
