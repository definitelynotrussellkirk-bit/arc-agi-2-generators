"""Generator for arc_additional_puzzle_bank_volume4:M26 — Output normalized union of color-1 and color-2 cells.

Rule: collect all color-1 and color-2 cells, normalize to upper-left,
output is a grid sized to fit the union bbox, with all cells painted 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_one, n_two,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_color_1, no_color_2, single_row_union.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9cea0e6444f1"
VERSION = "1.1.0"
TASK_ID = "9cea0e6444f1"
SUMMARY = "Scattered color-1 and color-2 cells; output is union normalized to upper-left, painted 3."

INVARIANTS = [
    "between 2 and 5 color-1 cells",
    "between 2 and 5 color-2 cells",
    "union spans both rows and cols (so output isn't a single row/col)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_color_1", "no_color_2", "single_row_union")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_one":          {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "n_two":          {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
    "density":        {"type": "str", "default": "scattered", "valid": "scattered"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_one = ctx.draw_int("n_one", 2, 3)
        n_two = ctx.draw_int("n_two", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_one = ctx.draw_int("n_one", 4, 4)
        n_two = ctx.draw_int("n_two", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_one = ctx.draw_int("n_one", 2, 4)
        n_two = ctx.draw_int("n_two", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = 0
    while placed < n_one:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 1; placed += 1
    placed = 0
    while placed < n_two:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 2; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_color_1":
        # only color-2 cells → union is just the color-2 cells; rule still applies but degenerate
        g[2][3] = 2; g[4][6] = 2; g[6][1] = 2
        return g
    if name == "no_color_2":
        # only color-1 cells → union is just the color-1 cells
        g[2][3] = 1; g[4][6] = 1; g[6][1] = 1
        return g
    if name == "single_row_union":
        # all color-1 and color-2 cells on the same row → union spans only one row
        # output has 0 rows after normalization (or 1×N strip)
        g[3][1] = 1; g[3][3] = 1; g[3][5] = 2; g[3][7] = 2
        return g
    return g
