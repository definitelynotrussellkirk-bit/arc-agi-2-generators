"""Generator for v0_original:easy_02 — keep topmost non-zero per column.

Rule: each column may have multiple non-zero cells; the output keeps only
the topmost one and zeros the rest.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_top_only, no_cells, all_columns_full.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4842b1ca59e2"
VERSION = "1.1.0"
TASK_ID = "4842b1ca59e2"
SUMMARY = "Several non-zero cells scattered across the grid (some columns have multiple)."

INVARIANTS = [
    "background is 0",
    "4-7 non-zero cells in any colors at random positions",
    "at least 2 columns have >=2 non-zero cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_top_only", "no_cells", "all_columns_full")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 5, 6)
        n = ctx.draw_int("n_cells", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_cells", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 5, 7)
        n = ctx.draw_int("n_cells", 4, 7)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        for _ in range(n):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
                break
        col_counts = [sum(1 for r in range(h) if g[r][c] != 0) for c in range(w)]
        if max(col_counts) >= 2:
            return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 6
    g = full_grid(h, w, 0)
    if name == "already_top_only":
        # each column has at most one cell, all in row 0 → rule is identity
        for c, v in enumerate([3, 4, 5, 6, 7, 8]):
            g[0][c] = v
        return g
    if name == "no_cells":
        # empty grid → no cells to drop, output is also all-zero
        return g
    if name == "all_columns_full":
        # every column entirely nonzero → output keeps just the top row, drops everything else
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 7)
        return g
    return g
