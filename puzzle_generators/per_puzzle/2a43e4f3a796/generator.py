"""Generator for arc_puzzle_bank_twelfth_21_bundle:easy_80_compact_columns_downward.

Rule: each column's nonzero cells drop to the bottom while preserving
top-to-bottom order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, all_at_bottom, single_value_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2a43e4f3a796"
VERSION = "1.1.0"
TASK_ID = "2a43e4f3a796"
SUMMARY = "Each column's nonzero cells drop to the bottom while preserving top-to-bottom order."

INVARIANTS = [
    "background is 0",
    "columns are processed independently",
    "nonzero values keep their top-to-bottom order",
    "at least one active column contains gaps below nonzero cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "all_at_bottom", "single_value_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "3..24"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "2..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_cols":    {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..8", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 6, 7)
        target = min(ctx.draw_int("active_cols", 3, 4), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("active_cols", 5, 6), w)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 6, 10)
        target = min(ctx.draw_int("active_cols", 3, 6), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in rng.sample(range(w), target):
        count = rng.randint(2, min(5, h - 1))
        rows = sorted(rng.sample(range(0, h - 1), count))
        for r in rows:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 8
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid → gravity has nothing to compact
        return g
    if name == "all_at_bottom":
        # cells already packed at bottom → rule is identity
        for c in [1, 3, 5]:
            g[h - 2][c] = 4
            g[h - 1][c] = 6
        return g
    if name == "single_value_columns":
        # each active column has only one cell → "preserve order" is trivial
        for c in [1, 3, 5]:
            g[3][c] = 4
        return g
    return g
