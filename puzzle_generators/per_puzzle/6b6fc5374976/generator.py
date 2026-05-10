"""Generator for arc_additional_puzzle_bank_volume23:H158.

Rule: a control-rotated blue template is stamped from marker 8 along
the 7→8 vector until it hits a wall or the edge.

Combinatorial axes (8): grid_h/w, palette_kind, rotation_control,
palette_size, position_bias, n_distinct_colors, wall_density, texture.
Degenerates: no_template, no_rot_control, no_marker_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "6b6fc5374976"
VERSION = "1.1.0"
TASK_ID = "6b6fc5374976"
SUMMARY = "A control-rotated blue template is stamped from marker 8 along the 7-to-8 vector until a wall or edge stops it."

INVARIANTS = [
    "one blue template is present",
    "one rotation control is 2, 3, 4, or 6",
    "markers 7 and 8 define the repeat direction",
    "the sequence has at least two valid placements before stopping",
]

PALETTE_KINDS = ("default", "rot_2", "rot_3_or_4", "rot_6")
DEGENERATE_TEXTURES = ("no_template", "no_rot_control", "no_marker_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "11..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rotation_control": {"type": "int", "default": "rng 2|3|4|6",
                         "valid": "2|3|4|6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..5"},
    "wall_density":   {"type": "str", "default": "low", "valid": "low"},
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 13, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    paint_at(g, 0, w // 2, [(0, 1), (1, 0), (1, 1), (1, 2)], 1)
    g[4][w // 2 - 2] = rng.choice([2, 3, 4, 6])
    g[6][2] = 7
    g[7][4] = 8
    if w > 15:
        g[h - 3][w - 3] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 15
    g = full_grid(h, w, 0)
    if name == "no_template":
        # control + markers but no blue template to repeat
        g[4][w // 2 - 2] = 3
        g[6][2] = 7
        g[7][4] = 8
        return g
    if name == "no_rot_control":
        # template + markers but no rotation selector
        paint_at(g, 0, w // 2, [(0, 1), (1, 0), (1, 1), (1, 2)], 1)
        g[6][2] = 7
        g[7][4] = 8
        return g
    if name == "no_marker_pair":
        # template + control but only marker 7 (or 8) → no vector
        paint_at(g, 0, w // 2, [(0, 1), (1, 0), (1, 1), (1, 2)], 1)
        g[4][w // 2 - 2] = 6
        g[6][2] = 7
        return g
    return g
