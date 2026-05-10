"""Generator for arc_puzzle_bank_seventeenth_21_bundle:easy_115_top_pack_each_column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, columns,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_top_packed, no_active_columns, single_cell_column.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e4b49ab9de5f"
VERSION = "1.1.0"
TASK_ID = "e4b49ab9de5f"
SUMMARY = "Scattered column values compact upward preserving vertical order."

INVARIANTS = [
    "background is 0",
    "active columns contain one to three nonzero values",
    "values start below the top row so packing changes the grid",
    "relative top-to-bottom order in each column is preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_top_packed", "no_active_columns", "single_cell_column")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "columns":        {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "below_top_row",
                       "valid": "below_top_row"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 6, 7)
        target = min(ctx.draw_int("columns", 3, 4), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("columns", 5, 6), w)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 6, 10)
        target = min(ctx.draw_int("columns", 3, 6), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in rng.sample(range(w), target):
        count = rng.randint(1, min(3, h - 1))
        for r in sorted(rng.sample(range(1, h), count)):
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "already_top_packed":
        # values already sit at the top → packing is identity, no visible movement
        for c in range(0, w, 2):
            g[0][c] = 4
            if c + 1 < w:
                g[1][c] = 5
        return g
    if name == "no_active_columns":
        # empty grid → no values to pack, rule no-op
        return g
    if name == "single_cell_column":
        # each column has at most one cell → packing reduces to top-row presence test
        for c in [1, 4, 6]:
            g[c][c] = 1 + (c % 5)
        return g
    return g
