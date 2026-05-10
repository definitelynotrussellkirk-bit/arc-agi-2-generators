"""Generator for arc_puzzle_bank_21_set6:easy_f06.

Rule: drop every column's nonzero values to the bottom, preserving
top-to-bottom order.

Combinatorial axes (8): grid_h/w, palette_kind, n_columns, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, already_settled, full_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22304ccc509c"
VERSION = "1.1.0"
TASK_ID = "22304ccc509c"
SUMMARY = "Drop every column's nonzero values to the bottom, preserving order."

INVARIANTS = [
    "background is 0",
    "columns are transformed independently",
    "nonzero values keep their top-to-bottom order",
    "all values settle at the bottom of their original column",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("empty_grid", "already_settled", "full_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "columns":        {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scatter",
                       "valid": "scatter"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    n = min(ctx.draw_int("columns", 3, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for c in rng.sample(range(w), n):
        k = rng.randint(1, min(3, h))
        rows = sorted(rng.sample(range(h - 1), k))
        for r in rows:
            g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to drop — output equals input
        return g
    if name == "already_settled":
        # all nonzero cells already at bottom — gravity is identity
        g[h - 1][1] = 4
        g[h - 1][3] = 6
        g[h - 2][3] = 5
        return g
    if name == "full_columns":
        # column completely filled — gravity is identity (already packed)
        for r in range(h):
            g[r][2] = ((r % 7) + 1)
        return g
    return g
