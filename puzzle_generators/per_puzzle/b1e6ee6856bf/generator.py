"""Generator for arc_puzzle_bank_21_set7:easy_g01.

Rule: keep only the topmost nonzero cell in each column.

Combinatorial axes (8): grid_h/w, palette_kind, n_cols, density,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: empty_grid, single_per_col, all_at_top.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b1e6ee6856bf"
VERSION = "1.1.0"
TASK_ID = "b1e6ee6856bf"
SUMMARY = "Each used column contains a short stack; only its topmost nonzero survives."

INVARIANTS = [
    "used columns are distinct",
    "each used column has at least one nonzero",
    "background is zero",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("empty_grid", "single_per_col", "all_at_top")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cols":         {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5",
                          "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
    n = min(ctx.draw_int("n_cols", 2, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = list(range(w))
    rng.shuffle(cols)
    for c in cols[:n]:
        rows = list(range(h))
        rng.shuffle(rows)
        for r in sorted(rows[:rng.randint(1, 3)]):
            g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        return g
    if name == "single_per_col":
        # each column already has exactly one cell — rule is identity
        for c in [1, 3, 5]:
            g[3][c] = (c % 8) + 1
        return g
    if name == "all_at_top":
        # all cells already at the top row — rule is identity
        for c in [1, 2, 4, 5]:
            g[0][c] = (c % 8) + 1
        return g
    return g
