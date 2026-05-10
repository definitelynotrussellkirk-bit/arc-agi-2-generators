"""Generator for arc_puzzle_bank_sixth21:E41.

Rule: each column's nonzero values are packed upward in original
top-to-bottom order.

Combinatorial axes (8): grid_h/w, palette_kind, n_cols, density,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: empty_grid, full_grid, already_packed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e9238d278276"
VERSION = "1.1.0"
TASK_ID = "e9238d278276"
SUMMARY = "Each column's nonzero values are packed upward in original top-to-bottom order."

INVARIANTS = [
    "columns contain scattered nonzero cells",
    "empty cells remain zero",
    "colors are preserved within columns",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("empty_grid", "full_grid", "already_packed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cols":         {"type": "int", "default": "rng 3..6", "valid": "1..10"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..8",
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
        w = ctx.draw_int("grid_w", 6, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
    n = min(ctx.draw_int("n_cols", 3, 6), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = list(range(w))
    rng.shuffle(cols)
    for c in cols[:n]:
        rows = list(range(h))
        rng.shuffle(rows)
        for i, r in enumerate(rows[:rng.randint(1, min(4, h))]):
            g[r][c] = (i % 8) + 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        return g
    if name == "full_grid":
        # no empty cells to pack into — rule is identity
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r + c) % 8) + 1
        return g
    if name == "already_packed":
        # cells already packed at the top of each column
        for c in range(w):
            g[0][c] = ((c % 8) + 1)
        for c in [1, 3, 5]:
            g[1][c] = 5
        return g
    return g
