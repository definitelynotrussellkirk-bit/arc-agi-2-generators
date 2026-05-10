"""Generator for arc_additional_puzzles_21_set16_bundle:E108.

Rule: rank rows by non-zero count (desc, ties by row index asc); output
the top-ranked row as a 1-row grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, max_count,
palette_size, position_bias, n_distinct_colors, count_spread, texture.
Degenerates: empty_grid, all_rows_equal, full_row_winner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7ffd4a6769a"
VERSION = "1.1.0"
TASK_ID = "f7ffd4a6769a"
SUMMARY = "Each row has a different count of non-bg cells; one row clearly has the most."

INVARIANTS = [
    "≥3 rows have varying non-zero counts (1, 2, 3, 4, ...)",
    "exactly one row has the maximum non-zero count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "all_rows_equal", "full_row_winner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "max_count":      {"type": "int", "default": "rng h..min(w,h+1)",
                       "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..8"},
    "count_spread":   {"type": "str", "default": "monotone", "valid": "monotone"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    counts = rng.sample(range(1, min(w, h + 2)), h)
    for r in range(h):
        cs = rng.sample(range(w), counts[r])
        for c in cs:
            g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # all rows have count 0 → "max" row is ambiguous (every row ties at zero)
        return g
    if name == "all_rows_equal":
        # every row has the same count → tie-break by row index, but rule expects unique max
        for r in range(h):
            for c in range(3):
                g[r][c] = 4
        return g
    if name == "full_row_winner":
        # winner row is fully filled; other rows empty → trivial recovery, no spread
        for c in range(w):
            g[2][c] = 5
        return g
    return g
