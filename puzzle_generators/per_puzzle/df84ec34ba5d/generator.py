"""Generator for arc_puzzle_bank_21_set7_s:S7_M6 — row majority column.

Rule: for each row, output the most-common non-zero value in that row
(ties: leftmost first occurrence). Output is Hx1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_majority,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_rows, no_majority, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df84ec34ba5d"
VERSION = "1.1.0"
TASK_ID = "df84ec34ba5d"
SUMMARY = "Dense rows of mixed colors with a clear majority per row."

INVARIANTS = [
    "background is 0",
    "every row's majority non-zero color is unambiguous (strict majority over other non-zero values)",
    "≥1 row has all zeros (so its majority is 0 — note the rule yields 0 for empty rows)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_rows", "no_majority", "all_distinct")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_majority":     {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 4..9", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "row_majority",
                       "valid": "row_majority"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..9", "valid": "2..9"},
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
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        if rng.random() < 0.2:
            continue  # all-zero row
        majority = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        n_majority = rng.randint(2, max(2, w // 2 + 1))
        cols = rng.sample(range(w), min(n_majority, w))
        for c in cols:
            g[r][c] = majority
        # add 1-2 distractors
        remaining = [c for c in range(w) if g[r][c] == 0]
        if remaining:
            n_dist = rng.randint(0, min(1, len(remaining)))
            for c in rng.sample(remaining, n_dist):
                g[r][c] = rng.choice([d for d in [1, 2, 3, 4, 5, 6, 7, 8, 9] if d != majority])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "empty_rows":
        # all rows blank → output column is all zeros, no signal
        return g
    if name == "no_majority":
        # row has 2 colors at equal counts → ambiguous majority
        for c in range(0, w, 2): g[0][c] = 4
        for c in range(1, w, 2): g[0][c] = 6
        return g
    if name == "all_distinct":
        # each row has all distinct colors → no majority, all tie
        for r in range(h):
            for c in range(w):
                g[r][c] = (r + c) % 9 + 1
        return g
    return g
