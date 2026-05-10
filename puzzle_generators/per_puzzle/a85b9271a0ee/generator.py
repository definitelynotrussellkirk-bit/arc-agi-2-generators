"""Generator for arc_puzzle_bank_21_more:easy_b05.

Rule: for each non-bg cell (r, c, v), set out[r+1][c+1] = v if
in-bounds. Output starts as empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, last_row_occupied, last_col_occupied.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "a85b9271a0ee"
VERSION = "1.1.0"
TASK_ID = "a85b9271a0ee"
SUMMARY = "A small connected shape with non-bg cells, away from bottom-right edge."

INVARIANTS = [
    "≥3 non-bg cells",
    "no non-bg cells in last row or last column (so all shift in-bounds)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "last_row_occupied", "last_col_occupied")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "top_left",
                       "valid": "top_left"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape = rng.choice([
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 1), (2, 0)],
    ])
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    top = rng.randint(0, h - 4)
    left = rng.randint(0, w - 3)
    paint_at(g, top, left, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to shift — output equals input
        return g
    if name == "last_row_occupied":
        # cells in the last row → their (r+1, c+1) targets are out-of-bounds
        for r, c in [(h - 1, 1), (h - 1, 2), (h - 2, 1)]:
            g[r][c] = 4
        return g
    if name == "last_col_occupied":
        # cells in the last col → their (r+1, c+1) targets are out-of-bounds
        for r, c in [(1, w - 1), (2, w - 1), (1, w - 2)]:
            g[r][c] = 5
        return g
    return g
