"""Generator for arc_additional_puzzle_bank_volume23:H155.

Rule: a control marker (4, 6, or 8) selects union, intersection, or
XOR of normalized color-2 and color-3 templates; the result is rendered
in maroon (color 9).

Combinatorial axes (8): grid_h/w, palette_kind, control_color,
palette_size, position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: no_control, no_template_2, no_template_3.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c30d1ebefb1f"
VERSION = "1.1.0"
TASK_ID = "c30d1ebefb1f"
SUMMARY = "A control selects union, intersection, or XOR of normalized color-2 and color-3 templates, rendered in maroon."

INVARIANTS = [
    "one control marker is 4, 6, or 8",
    "one color-2 template and one color-3 template are present",
    "the normalized templates partially overlap",
    "the result is cropped and painted color 9",
]

PALETTE_KINDS = ("default", "control_4", "control_6", "control_8")
DEGENERATE_TEXTURES = ("no_control", "no_template_2", "no_template_3")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng 4|6|8", "valid": "4|6|8"},
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 13, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[h - 3][w - 2] = rng.choice([4, 6, 8])
    a = [(0, 0), (1, 0), (2, 0), (2, 1)]
    b = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, 2, w - 5, a, 2)
    paint_at(g, 1, 1, b, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 15
    g = full_grid(h, w, 0)
    a = [(0, 0), (1, 0), (2, 0), (2, 1)]
    b = [(0, 0), (0, 1), (1, 1), (2, 1)]
    if name == "no_control":
        # both templates but no control — operation undefined
        paint_at(g, 2, w - 5, a, 2)
        paint_at(g, 1, 1, b, 3)
        return g
    if name == "no_template_2":
        # control + only color-3 template — boolean op has no operand
        g[h - 3][w - 2] = 6
        paint_at(g, 1, 1, b, 3)
        return g
    if name == "no_template_3":
        # control + only color-2 template — boolean op has no operand
        g[h - 3][w - 2] = 4
        paint_at(g, 2, w - 5, a, 2)
        return g
    return g
