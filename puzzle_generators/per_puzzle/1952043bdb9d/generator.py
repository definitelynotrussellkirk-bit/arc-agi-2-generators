"""Generator for arc_puzzle_bank_21_next:easy_c02 — Per column, keep only the bottommost non-bg cell.

Rule: for each column, find the lowest row with a non-zero cell;
keep only that cell, zero out the rest.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_columns,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, all_at_bottom, full_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1952043bdb9d"
VERSION = "1.1.0"
TASK_ID = "1952043bdb9d"
SUMMARY = "Per column, multiple non-bg cells of varying colors."

INVARIANTS = [
    "≥3 columns have ≥2 non-zero cells (so output differs from input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "all_at_bottom", "full_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_columns":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "stacked_columns",
                       "valid": "stacked_columns"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    cols_with_2plus = rng.sample(range(w), rng.randint(3, 4))
    for c in cols_with_2plus:
        n = rng.randint(2, 3)
        rs = rng.sample(range(h), n)
        for r in rs:
            g[r][c] = rng.choice(palette)
    other_cols = [c for c in range(w) if c not in cols_with_2plus]
    for c in other_cols:
        if rng.random() < 0.5:
            r = rng.randint(0, h - 1)
            g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # every column has at most one cell → "bottommost" is that cell, rule is identity
        g[2][1] = 4; g[5][3] = 6; g[3][5] = 3
        return g
    if name == "all_at_bottom":
        # every nonzero already on bottom row → rule is identity
        for c in [1, 3, 5]:
            g[h - 1][c] = (c % 8) + 1
        return g
    if name == "full_columns":
        # active columns completely filled → rule keeps just the bottom cell, dropping h-1 cells
        for c in [1, 4]:
            for r in range(h):
                g[r][c] = (c % 8) + 1
        return g
    return g
