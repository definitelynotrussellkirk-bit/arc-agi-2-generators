"""Generator for medium_57_sort_rows_by_occupancy.

Rule: sort the rows of the grid by descending non-zero occupancy.

Combinatorial axes (8): grid_h/w, palette_kind, occupancy_spread,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_equal_counts, already_sorted, all_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "323fded12174"
VERSION = "1.1.0"
TASK_ID = "323fded12174"
SUMMARY = "Rows of varying occupancy (sparse → dense)."

INVARIANTS = [
    "background is 0",
    "row occupancy varies (≥2 distinct fill counts)",
]

PALETTE_KINDS = ("varied_occupancy", "stepped", "scrambled", "rainbow")
DEGENERATE_TEXTURES = ("all_equal_counts", "already_sorted", "all_zero")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "occupancy_spread": {"type": "str", "default": "wide",
                         "valid": "tight|wide"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "uniform", "valid": "uniform"},
    "n_distinct_colors": {"type": "int", "default": "9", "valid": "9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    counts = list(range(0, w))
    rng.shuffle(counts)
    counts = counts[:h]
    for r, count in enumerate(counts):
        cols = rng.sample(range(w), min(count, w))
        for c in cols:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "all_equal_counts":
        for r in range(h):
            for c in range(3):
                g[r][c] = 5
        return g
    if name == "already_sorted":
        for r in range(h):
            count = max(0, w - r - 1)
            for c in range(count):
                g[r][c] = 5
        return g
    if name == "all_zero":
        return g
    return g
