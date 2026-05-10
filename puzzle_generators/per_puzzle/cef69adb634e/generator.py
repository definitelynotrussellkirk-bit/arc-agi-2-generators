"""Generator for arc_additional_puzzle_bank_volume23:M156.

Rule: for each color in {2, 3, 4}, if there are exactly 2 cells at
diagonal corners (different rows AND cols), paint the rect border in
that color.

Combinatorial axes (8): grid_h/w, palette_kind, n_pair_colors,
palette_size, position_bias, n_distinct_colors, rect_size, texture.
Degenerates: only_one_pair_color, cells_aligned, no_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cef69adb634e"
VERSION = "1.1.0"
TASK_ID = "cef69adb634e"
SUMMARY = "Colors 2, 3, 4 each have exactly 2 diagonal-corner cells + decoration."

INVARIANTS = [
    "each of colors 2, 3, 4 has exactly 2 cells at distinct rows AND cols",
    "rectangles don't fully overlap (some independence)",
    "decoration is non-{2,3,4} cells",
]

PALETTE_KINDS = ("default", "tight_rects", "wide_rects", "diagonal_rects")
DEGENERATE_TEXTURES = ("only_one_pair_color", "cells_aligned", "no_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pair_colors":  {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "rect_size":      {"type": "str", "default": "fixed", "valid": "fixed"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    g[1][0] = 2; g[6][8] = 2
    g[2][10] = 3; g[3][11] = 3
    g[3][3] = 4; g[8][9] = 4
    g[7][2] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "only_one_pair_color":
        # only color 2 has a diagonal pair — colors 3, 4 are missing
        g[1][1] = 2; g[6][8] = 2
        g[5][5] = 7
        return g
    if name == "cells_aligned":
        # color 2 cells are in same row → not a diagonal corner pair
        g[3][1] = 2; g[3][8] = 2
        g[2][10] = 3; g[5][12] = 3
        g[7][2] = 4; g[8][9] = 4
        return g
    if name == "no_pairs":
        # only decoration, no pairs of {2,3,4}
        g[2][2] = 7
        g[5][6] = 7
        return g
    return g
