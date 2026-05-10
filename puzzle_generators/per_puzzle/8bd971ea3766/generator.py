"""Generator for arc_puzzle_bank_twentythird21:E156.

Rule: for each row, find triples (a, 0, a) where two non-zero same-color
cells flank a 0 with one cell in between; fill the 0 with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_triples, no_gap, no_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8bd971ea3766"
VERSION = "1.1.0"
TASK_ID = "8bd971ea3766"
SUMMARY = "1-3 rows each contain a 'X 0 X' triple in some color."

INVARIANTS = [
    "background is 0",
    "at least 1 row has cells (a, _, b, _, a) — i.e., (color 0 color) triple",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triples", "no_gap", "no_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "row_triples",
                       "valid": "row_triples"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_rows", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_rows", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 6, 8)
        n = ctx.draw_int("n_rows", 1, min(3, h))
    n = min(n, h)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for r, color in zip(rows, colors):
        c0 = rng.randint(0, w - 3)
        g[r][c0] = color
        g[r][c0 + 2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "no_triples":
        # nonzero cells exist but never form (a, 0, a) → rule has no targets
        g[1][1] = 4
        g[2][3] = 5
        g[3][5] = 6
        return g
    if name == "no_gap":
        # potential triple is (a, a, a) instead of (a, 0, a) → middle cell already occupied
        g[1][1] = 4; g[1][2] = 4; g[1][3] = 4
        return g
    if name == "no_rows":
        # empty grid → no rows to scan
        return g
    return g
