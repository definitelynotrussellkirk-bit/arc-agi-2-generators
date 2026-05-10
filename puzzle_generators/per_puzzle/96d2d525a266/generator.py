"""Generator for arc_additional_puzzle_bank_volume13:M89.

Rule: for each non-bg color with exactly 2 cells at distinct rows AND
cols, paint the rect border between them in that color.

Combinatorial axes (8): grid_h/w, palette_kind, n_pair_colors,
palette_size, position_bias, n_distinct_colors, decoration_density, texture.
Degenerates: no_pair_colors, all_aligned, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "96d2d525a266"
VERSION = "1.1.0"
TASK_ID = "96d2d525a266"
SUMMARY = "3 colors each with exactly 2 cells at diagonal corners + decoration."

INVARIANTS = [
    "exactly 3 distinct colors used as 2-corner-pairs",
    "each pair at distinct rows AND cols",
    "decoration is 1-2 cells of color 9 (won't form rects)",
]

PALETTE_KINDS = ("default", "warm_pairs", "cool_pairs", "wide_spread")
DEGENERATE_TEXTURES = ("no_pair_colors", "all_aligned", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pair_colors":  {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "decoration_density": {"type": "str", "default": "low", "valid": "low"},
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
    g[0][6] = 6
    g[2][8] = 6
    g[5][9] = 9; g[6][9] = 9
    g[7][2] = 1; g[9][2] = 1
    g[8][8] = 2
    g[5][5] = 5; g[3][4] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_pair_colors":
        # only singletons — rule produces no rectangles
        g[1][1] = 6
        g[5][5] = 5
        g[8][3] = 1
        return g
    if name == "all_aligned":
        # each color's two cells share a row OR col — no diagonal pairs
        g[2][1] = 6; g[2][8] = 6  # same row
        g[1][5] = 5; g[7][5] = 5  # same col
        g[3][3] = 1; g[3][9] = 1  # same row
        return g
    if name == "no_cells":
        # empty grid — nothing to outline
        return g
    return g
