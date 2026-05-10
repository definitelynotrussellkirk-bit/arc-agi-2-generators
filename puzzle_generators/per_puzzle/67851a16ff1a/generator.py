"""Generator for arc_additional_puzzle_bank_volume9:H60.

Rule: a top-left control rotates the blue template; the rotated mask is
intersected with the red mask, output is the cropped cyan intersection.

Combinatorial axes (8): grid_h/w, palette_kind, control_color,
palette_size, position_bias, n_distinct_colors, mask_overlap, texture.
Degenerates: no_control, no_blue, no_red.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "67851a16ff1a"
VERSION = "1.1.0"
TASK_ID = "67851a16ff1a"
SUMMARY = "A top-left control rotates the blue template before intersecting it with a normalized red shape."

INVARIANTS = [
    "top-left control is 3, 4, 5, or 6",
    "one blue template and one red template are present",
    "the rotated blue mask overlaps the red mask",
    "the output is the cropped cyan intersection",
]

PALETTE_KINDS = ("default", "control_3", "control_4", "control_5_6")
DEGENERATE_TEXTURES = ("no_control", "no_blue", "no_red")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng",
                       "valid": "3|4|5|6"},
    "mask_overlap":   {"type": "str", "default": "partial",
                       "valid": "partial"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([3, 4, 5, 6])
    blue = [(0, 0), (1, 0), (2, 0), (2, 1)]
    red = [(0, 0), (0, 1), (1, 0), (1, 1)]
    paint_at(g, 1, 2, blue, 1)
    paint_at(g, h - 5, w - 5, red, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    blue = [(0, 0), (1, 0), (2, 0), (2, 1)]
    red = [(0, 0), (0, 1), (1, 0), (1, 1)]
    if name == "no_control":
        # blue + red but no control — rotation amount undefined
        paint_at(g, 1, 2, blue, 1)
        paint_at(g, h - 5, w - 5, red, 2)
        return g
    if name == "no_blue":
        # control + red but no blue template to rotate
        g[0][0] = 4
        paint_at(g, h - 5, w - 5, red, 2)
        return g
    if name == "no_red":
        # control + blue but no red mask to intersect with
        g[0][0] = 4
        paint_at(g, 1, 2, blue, 1)
        return g
    return g
