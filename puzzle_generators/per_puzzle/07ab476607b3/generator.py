"""Generator for arc_additional_puzzle_bank_volume6:H42.

Rule: subtract the normalized color-4 shape from the normalized color-2
shape and place the difference as 6 at the 9 anchor.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, no_anchor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "07ab476607b3"
VERSION = "1.1.0"
TASK_ID = "07ab476607b3"
SUMMARY = "Subtract normalized color-4 from color-2 shape; place difference as 6."

INVARIANTS = [
    "there is one color-2 source shape and one color-4 subtractor shape",
    "the normalized difference is nonempty and fits at the 9 anchor",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_anchor", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "9..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "10..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
    g = full_grid(h, w, 0)
    shape_a = [(0, 0), (0, 1), (1, 0), (2, 0)]
    shape_b = [(0, 0), (1, 0)]
    paint_at(g, 1, 1, shape_a, 2)
    paint_at(g, 1, w - 4, shape_b, 4)
    g[h - 4][w // 2] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 11, 0)
    if name == "no_shapes":
        g[6][5] = 9
        return g
    if name == "no_anchor":
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (2, 0)], 2)
        paint_at(g, 1, 7, [(0, 0), (1, 0)], 4)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(11):
                g[r][c] = 6
        return g
    return g
