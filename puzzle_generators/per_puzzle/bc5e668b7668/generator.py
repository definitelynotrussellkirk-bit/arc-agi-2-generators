"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_130_up_pack_each_column_preserving_order.

Rule: each column's nonzero values pack upward, preserving order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, columns,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_at_top, all_singletons, full_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bc5e668b7668"
VERSION = "1.1.0"
TASK_ID = "bc5e668b7668"
SUMMARY = "Columns contain scattered values that compact upward in place."

INVARIANTS = [
    "background is 0",
    "each active column has one to three nonzero values",
    "at least one active column has a zero above a value",
    "relative top-to-bottom order in each column is meaningful",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_at_top", "all_singletons", "full_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "columns":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_columns",
                       "valid": "scattered_columns"},
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
        w = ctx.draw_int("grid_w", 6, 7)
        target = min(ctx.draw_int("columns", 2, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target = min(ctx.draw_int("columns", 4, 5), w)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 6, 9)
        target = min(ctx.draw_int("columns", 3, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    columns = rng.sample(range(w), target)
    for c in columns:
        count = rng.randint(1, min(3, h - 1))
        rows = sorted(rng.sample(range(1, h), count))
        for r in rows:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "all_at_top":
        # all column values already top-packed → rule is identity
        g[0][1] = 4; g[1][1] = 6
        g[0][3] = 3; g[1][3] = 8
        return g
    if name == "all_singletons":
        # each column has one value → pack-up is identity at the value, preserves position
        # rule trivially also is identity if value already at row 0; here it shifts to top
        g[3][1] = 4; g[4][3] = 6; g[5][5] = 3
        return g
    if name == "full_columns":
        # active columns completely full → rule is identity (no zeros to pack into)
        for c in [1, 4]:
            for r in range(h):
                g[r][c] = (c % 8) + 1
        return g
    return g
