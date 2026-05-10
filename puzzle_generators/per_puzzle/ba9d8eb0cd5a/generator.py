"""Generator for arc_puzzle_bank_twentieth_21_bundle:easy_137_left_pack_rows_preserving_order.

Rule: each row's nonzero cells are packed left while preserving order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, already_packed, single_per_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ba9d8eb0cd5a"
VERSION = "1.1.0"
TASK_ID = "ba9d8eb0cd5a"
SUMMARY = "Each row's nonzero cells are packed left while preserving order."

INVARIANTS = [
    "background is 0",
    "rows are independent",
    "nonzero row order is preserved",
    "at least one active row starts with a zero gap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "already_packed", "single_per_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "2..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "3..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rows":           {"type": "int", "default": "rng 3..6", "valid": "1..12"},
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
        target = min(ctx.draw_int("rows", 3, 4), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 14)
        target = min(ctx.draw_int("rows", 5, 6), h)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 14)
        target = min(ctx.draw_int("rows", 3, 6), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), target):
        count = rng.randint(2, min(5, w - 1))
        cols = sorted(rng.sample(range(1, w), count))
        for c in cols:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to pack — output equals input
        return g
    if name == "already_packed":
        # all nonzero cells are already left-packed → rule has no visible effect
        for r, vals in [(1, [3, 4, 5]), (3, [2, 7]), (5, [6, 8, 9, 1])]:
            for i, v in enumerate(vals):
                g[r][i] = v
        return g
    if name == "single_per_row":
        # each row has at most one nonzero cell → packing reduces to a single shift
        g[1][5] = 3
        g[3][8] = 6
        g[5][2] = 4
        return g
    return g
