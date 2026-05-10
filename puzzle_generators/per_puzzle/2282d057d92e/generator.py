"""Generator for arc_puzzle_bank_21_set23_bundle:easy_p02.

Rule: sparse row seeds cast their colors rightward until the next seed
or border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, all_at_right_edge, single_seed_per_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2282d057d92e"
VERSION = "1.1.0"
TASK_ID = "2282d057d92e"
SUMMARY = "Sparse row seeds cast their colors rightward until the next seed."

INVARIANTS = [
    "background is 0",
    "active rows contain one to three nonzero seeds",
    "each seed has at least one empty cell to its right unless it is a stopper",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "all_at_right_edge", "single_seed_per_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_seeds",
                       "valid": "row_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        w = ctx.draw_int("grid_w", 9, 11)
        row_count = min(ctx.draw_int("row_count", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        row_count = min(ctx.draw_int("row_count", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        row_count = min(ctx.draw_int("row_count", 3, 5), h)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for row_index, r in enumerate(rows):
        seed_count = rng.randint(1, 3)
        cols = sorted(rng.sample(range(w), seed_count))
        colors = rng.sample(palette, seed_count)
        for c, color in zip(cols, colors):
            grid[r][c] = color
        if seed_count == 1 and cols[0] == w - 1:
            grid[r][w - 2] = palette[row_index % len(palette)]
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank grid → no seeds to cast, rule is identity
        return g
    if name == "all_at_right_edge":
        # all seeds on the last column → no cell to their right, casts extend 0 cells
        g[1][w - 1] = 4
        g[3][w - 1] = 6
        g[5][w - 1] = 3
        return g
    if name == "single_seed_per_row":
        # one seed per row with no stopper → cast extends all the way to the right border
        # rule effect spans the entire row to the right of seed
        g[1][2] = 4
        g[3][1] = 6
        g[5][3] = 3
        return g
    return g
