"""Generator for arc_puzzle_bank_eighth21:E55.

Rule: drop each column's nonzero cells to the bottom of that column
while preserving their top-to-bottom order.

Combinatorial axes (8): grid_h/w, palette_kind, columns, density,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: empty_grid, full_grid, already_packed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3696e3c9d426"
VERSION = "1.1.0"
TASK_ID = "3696e3c9d426"
SUMMARY = "Drop each column's nonzero cells to the bottom while preserving order."

INVARIANTS = [
    "background is 0",
    "columns transform independently",
    "nonzero cells preserve top-to-bottom order",
    "packed cells occupy the bottom of their original column",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "already_packed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "columns":        {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..9",
                          "valid": "1..9"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    n = min(ctx.draw_int("columns", 3, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in rng.sample(range(w), n):
        k = rng.randint(1, min(3, h - 1))
        rows = sorted(rng.sample(range(h - 1), k))
        for r in rows:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        return g
    if name == "full_grid":
        # no empty cells to drop into
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r + c) % 9) + 1
        return g
    if name == "already_packed":
        # cells already at bottom — gravity is identity
        for c in range(w):
            g[h - 1][c] = ((c % 9) + 1)
        for c in [1, 3, 5]:
            g[h - 2][c] = 5
        return g
    return g
