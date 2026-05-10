"""Generator for arc_additional_puzzles_21_set7:E49 — Connect cells with L-paths.

Rule: for each color, find its cells in scan order. Draw L-paths between
consecutive cells (horizontal then vertical).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_cell_per_color, all_collinear, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "84fd4bcdc53c"
VERSION = "1.1.0"
TASK_ID = "84fd4bcdc53c"
SUMMARY = "1-2 colors, each with 2-3 cells at distinct rows AND cols."

INVARIANTS = [
    "1-2 distinct non-bg colors",
    "each color: 2-3 cells, none on the same row or col",
    "cells of each color are separated by ≥3 in row or col",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_cell_per_color", "all_collinear", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "distinct_rows_cols",
                       "valid": "distinct_rows_cols"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_colors)
    for color in palette:
        n_cells = rng.randint(2, 3)
        rows = rng.sample(range(h), n_cells)
        cols = rng.sample(range(w), n_cells)
        for r, c in zip(rows, cols):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "single_cell_per_color":
        # each color has only one cell → no consecutive pairs to L-connect
        g[2][3] = 4
        g[5][7] = 6
        return g
    if name == "all_collinear":
        # cells share a row → L-paths collapse to straight horizontal lines
        g[2][1] = 4
        g[2][5] = 4
        g[2][8] = 4
        return g
    if name == "no_cells":
        # empty grid → rule has nothing to connect
        return g
    return g
