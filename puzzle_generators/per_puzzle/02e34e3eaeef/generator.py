"""Generator for arc_puzzle_bank_fifteenth_21_bundle:easy_104_read_singleton_colors_left_to_right.

Rule: scatter unique singleton colors; output reads them by column
then row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, duplicate_colors, all_one_column.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "02e34e3eaeef"
VERSION = "1.1.0"
TASK_ID = "02e34e3eaeef"
SUMMARY = "Scatter unique singleton colors; output reads them by column then row."

INVARIANTS = [
    "background is 0",
    "all nonzero cells are singletons",
    "colors are unique",
    "output is one row of colors ordered left to right",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "duplicate_colors", "all_one_column")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("markers", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("markers", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 12)
        target = ctx.draw_int("markers", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], k=target)
    positions = rng.sample([(r, c) for r in range(h) for c in range(w)], target)
    for color, (r, c) in zip(colors, positions):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to read — output is an empty row
        return g
    if name == "duplicate_colors":
        # repeated colors break "unique singleton" invariant
        g[2][1] = 3
        g[4][5] = 3
        g[5][7] = 6
        return g
    if name == "all_one_column":
        # all markers share one column → "left to right" ordering reduces to row order
        for r, v in [(0, 3), (2, 5), (4, 7), (6, 9)]:
            g[r][4] = v
        return g
    return g
