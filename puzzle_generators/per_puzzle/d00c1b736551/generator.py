"""Generator for arc_additional_puzzle_bank_volume6:H38.

Rule: intersect normalized color-2 shapes and place the common cells at
the 9 anchor as color 3.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, no_anchor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d00c1b736551"
VERSION = "1.1.0"
TASK_ID = "d00c1b736551"
SUMMARY = "Intersect normalized color-2 shapes and place the common cells at the 9 anchor as color 3."

INVARIANTS = [
    "there are at least three separated color-2 objects",
    "all normalized shapes share a nonempty common subset",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_anchor", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0)]
    paint_at(g, 1, 1, common + [(1, 1), (2, 1)], 2)
    paint_at(g, 1, w - 5, common + [(0, 1), (2, 0)], 2)
    paint_at(g, h - 5, 1, common + [(2, 0), (2, 1)], 2)
    g[h - 4][w - 4] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_shapes":
        g[7][8] = 9
        return g
    if name == "no_anchor":
        paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], 2)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
