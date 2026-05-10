"""Generator for arc_additional_puzzle_bank_volume2:E9.

Rule: zero cells horizontally between two color-1 cells become color 1.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors, other.
Degenerates: no_pattern, single_one, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3bb94038f4e2"
VERSION = "1.1.0"
TASK_ID = "3bb94038f4e2"
SUMMARY = "Zero cells horizontally between two color-1 cells become color 1."

INVARIANTS = [
    "there are multiple 1-0-1 horizontal patterns",
    "non-participating colors do not affect the fill",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "single_one", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "other":          {"type": "color", "default": "rng !{0,1}",
                       "valid": "2..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    other = ctx.draw_color("other", exclude=[0, 1])
    g = full_grid(h, w, 0)
    for r in [1, h // 2, h - 2]:
        g[r][2] = 1
        g[r][4] = 1
    g[0][w - 1] = other
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 8, 0)
    if name == "no_pattern":
        return g
    if name == "single_one":
        g[3][3] = 1
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(8):
                g[r][c] = 1
        return g
    return g
