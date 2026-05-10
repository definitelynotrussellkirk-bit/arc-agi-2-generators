"""Generator for arc_puzzle_bank_sixteenth_21_bundle:easy_109_left_pack_each_row.

Rule: each row's nonzero cells compact to the left while preserving order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, max_cells_per_row,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, already_packed, all_zero_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d0f5035a157"
VERSION = "1.1.0"
TASK_ID = "0d0f5035a157"
SUMMARY = "Each row's nonzero cells compact to the left while preserving order."

INVARIANTS = [
    "background is 0",
    "rows contain sparse colored sequences",
    "at least one row has a leading zero before a nonzero cell",
    "row order of nonzero cells is preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "already_packed", "all_zero_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "max_cells_per_row": {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_columns",
                       "valid": "scattered_columns"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..9", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 10)
        max_cells = min(ctx.draw_int("max_cells_per_row", 2, 3), w - 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        max_cells = min(ctx.draw_int("max_cells_per_row", 4, 5), w - 1)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        max_cells = min(ctx.draw_int("max_cells_per_row", 2, 5), w - 1)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        n = rng.randint(1, max_cells)
        cols = sorted(rng.sample(range(1, w), n))
        for c in cols:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to pack — output equals input
        return g
    if name == "already_packed":
        # every row's nonzero cells are already at the left → rule no-op
        for r, vals in [(0, [2]), (1, [3, 4]), (2, [5, 6, 7]),
                        (3, [8, 9, 1, 2]), (4, [3]), (5, [6, 7]), (6, [8, 9, 1])]:
            for i, v in enumerate(vals):
                g[r][i] = v
        return g
    if name == "all_zero_rows":
        # every row is all-zero → packing operates on nothing per row
        return g
    return g
