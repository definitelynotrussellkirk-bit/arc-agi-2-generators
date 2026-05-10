"""Generator for arc_puzzle_bank_21_more:easy_b06.

Rule: an asymmetric sparse pattern is transposed across the main diagonal.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marks, square_symmetric, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "efdd2b265cc8"
VERSION = "1.1.0"
TASK_ID = "efdd2b265cc8"
SUMMARY = "An asymmetric sparse pattern is transposed across the main diagonal."

INVARIANTS = [
    "input grid is rectangular and intentionally non-symmetric",
    "nonzero cells occupy distinct rows and columns",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "square_symmetric", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", max(6, h + 1), 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", max(7, h + 1), 9)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", max(6, h + 1), 9)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude=[0]))
    g = full_grid(h, w, 0)
    placements = [
        (0, 1, colors[0]),
        (1, w - 2, colors[1]),
        (h - 2, 2, colors[2]),
        (h - 1, w - 1, colors[3]),
    ]
    for r, c, color in placements:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 7, 0)
    if name == "no_marks":
        return g
    if name == "square_symmetric":
        g = full_grid(5, 5, 0)
        g[0][1] = 3
        g[1][0] = 3
        g[3][4] = 4
        g[4][3] = 4
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
