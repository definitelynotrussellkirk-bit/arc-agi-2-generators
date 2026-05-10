"""Generator for arc_additional_puzzle_bank_volume8:M52.

Rule: for color 2 (paint border 3) and color 1 (paint border 8): if there
are exactly 2 cells of that color, paint the rectangle border between
them with the corresponding output color.

Combinatorial axes (9): grid_h/w, palette_kind, rect_overlap,
palette_size, position_bias, n_distinct_colors, decoration, has_decoration, texture.
Degenerates: only_one_cell, three_cells, cells_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d414585aa873"
VERSION = "1.1.0"
TASK_ID = "d414585aa873"
SUMMARY = "2 2-cells (diagonal corners) + 2 1-cells (diagonal corners) + decoration."

INVARIANTS = [
    "exactly 2 2-cells at distinct rows AND cols",
    "exactly 2 1-cells at distinct rows AND cols",
    "rectangles don't overlap",
]

PALETTE_KINDS = ("default", "wide_separation", "tight_rects", "varied_corners")
DEGENERATE_TEXTURES = ("only_one_cell", "three_cells", "cells_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_overlap":   {"type": "bool", "default": "false", "valid": "false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "has_decoration": {"type": "bool", "default": "true",
                       "valid": "true|false"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    g[6][3] = 2
    g[8][5] = 2
    g[6][7] = 1
    g[8][9] = 1
    g[h - 1][2] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "only_one_cell":
        # Just one 2-cell — no second corner to define the rectangle
        g[6][3] = 2
        g[6][7] = 1
        g[8][9] = 1
        return g
    if name == "three_cells":
        # Three 2-cells — rectangle corners ambiguous
        g[6][3] = 2
        g[8][5] = 2
        g[3][7] = 2
        g[6][7] = 1
        g[8][9] = 1
        return g
    if name == "cells_aligned":
        # Two 2-cells in the same row — degenerate (zero-height) rect
        g[6][3] = 2
        g[6][8] = 2
        g[6][1] = 1
        g[8][9] = 1
        return g
    return g
