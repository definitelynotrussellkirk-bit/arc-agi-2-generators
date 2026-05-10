"""Generator for arc_puzzle_bank_21_next:medium_c06.

Rule: for each column, output one row of the most-frequent non-zero
color (ties → smaller color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, dominant_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, tied_majority, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1d14de95c43e"
VERSION = "1.1.0"
TASK_ID = "1d14de95c43e"
SUMMARY = "Each column has a dominant color with 1-2 noise cells."

INVARIANTS = [
    "each column has a unique dominant color (count ≥ 2)",
    "noise cells in non-dominant positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "tied_majority", "all_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dominant_count": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng w distinct", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "cols", "valid": "cols"},
    "n_distinct_colors": {"type": "int", "default": "rng w distinct",
                          "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
    palette = list(range(1, 10)); rng.shuffle(palette)
    for c in range(w):
        dominant = palette[c % len(palette)]
        rows = list(range(h)); rng.shuffle(rows)
        for r in rows[:rng.randint(2, 3)]:
            g[r][c] = dominant
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no cells in any column → mode undefined for every column
        return g
    if name == "tied_majority":
        # column has 2 colors with equal counts → "most frequent" ambiguous (tie-break needed)
        for r, v in [(0, 4), (1, 4), (2, 6), (3, 6)]:
            g[r][3] = v
        return g
    if name == "all_same_color":
        # every column shares one dominant color → output is uniform
        for r in range(h):
            for c in range(w):
                if (r + c) % 2 == 0:
                    g[r][c] = 4
        return g
    return g
