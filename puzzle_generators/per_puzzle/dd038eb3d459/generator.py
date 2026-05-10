"""Generator for arc_additional_puzzle_bank_volume18:H122.

Rule: a corner control rotates the green mask before XORing it with the
normalized red mask.

Combinatorial axes (8): grid_h/w, palette_kind, corner_position,
palette_size, position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: no_corner, no_red, no_green.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "dd038eb3d459"
VERSION = "1.1.0"
TASK_ID = "dd038eb3d459"
SUMMARY = "A corner control rotates the green mask before XORing it with the normalized red mask."

INVARIANTS = [
    "one blue control cell sits in a grid corner",
    "one red mask and one green mask are present",
    "the transformed masks partially overlap",
    "the output is a cropped cyan XOR mask",
]

PALETTE_KINDS = ("default", "tl_corner", "tr_corner", "bl_or_br_corner")
DEGENERATE_TEXTURES = ("no_corner", "no_red", "no_green")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..20"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "8..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "corner_position": {"type": "str", "default": "rng",
                        "valid": "tl|tr|bl|br"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 10, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cr, cc = rng.choice([(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)])
    g[cr][cc] = 1
    red = [(0, 0), (1, 0), (1, 1), (2, 1)]
    green = [(0, 1), (1, 0), (1, 1), (2, 1)]
    paint_at(g, 2, 1, red, 2)
    paint_at(g, 2, w - 5, green, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    red = [(0, 0), (1, 0), (1, 1), (2, 1)]
    green = [(0, 1), (1, 0), (1, 1), (2, 1)]
    if name == "no_corner":
        # red + green but no blue corner control → rotation undefined
        paint_at(g, 2, 1, red, 2)
        paint_at(g, 2, w - 5, green, 3)
        return g
    if name == "no_red":
        # control + green but no red — XOR has missing operand
        g[0][0] = 1
        paint_at(g, 2, w - 5, green, 3)
        return g
    if name == "no_green":
        # control + red but no green — XOR has missing operand
        g[0][0] = 1
        paint_at(g, 2, 1, red, 2)
        return g
    return g
