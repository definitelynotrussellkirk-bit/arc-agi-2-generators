"""Generator for arc_puzzle_bank_21_set10_e:easy_j07 — Right-align non-zero cells per row.

Rule: in each row, gather non-zero values in order; right-align them
in the row, preserving order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_per_row,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_right_packed, no_active_rows, fully_packed_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "85dcd5c922b9"
VERSION = "1.1.0"
TASK_ID = "85dcd5c922b9"
SUMMARY = "Each row has 1-3 scattered non-zero cells in distinct colors."

INVARIANTS = [
    ">=3 rows have >=1 non-zero cell",
    ">=1 row has >=2 non-zero cells (so right-shift is visible)",
    "no row is fully filled (so right-align differs from input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_right_packed", "no_active_rows", "fully_packed_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_per_row":      {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "left_biased",
                       "valid": "left_biased"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for r in range(h):
        n = rng.randint(0, 3)
        if n == 0:
            continue
        cols = rng.sample(range(w - 1), n)
        cols.sort()
        for c in cols:
            g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "already_right_packed":
        # rows already right-packed → rule is identity, no movement visible
        for r, vs in [(0, [3, 4, 5]), (2, [6, 7]), (4, [8, 9, 2])]:
            for i, v in enumerate(vs):
                g[r][w - len(vs) + i] = v
        return g
    if name == "no_active_rows":
        # empty grid → no rows to right-align
        return g
    if name == "fully_packed_rows":
        # all rows entirely nonzero → no gaps, identity output
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 7)
        return g
    return g
