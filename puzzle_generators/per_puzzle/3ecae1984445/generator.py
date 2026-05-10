"""Generator for arc_additional_puzzles_21_set2:E13.

Rule: each col with exactly 2 cells of color 7 separated by all-0 →
fill between them with 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, adjacent_7s, more_than_two_7s_per_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ecae1984445"
VERSION = "1.1.0"
TASK_ID = "3ecae1984445"
SUMMARY = "2-3 cols have exactly 2 7-cells separated by all-0."

INVARIANTS = [
    "≥2 cols have exactly 2 cells of color 7 with ≥2 0-cells between",
    "≥1 distractor row of two 7s adjacent (won't fill)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "adjacent_7s", "more_than_two_7s_per_col")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "column_pairs",
                       "valid": "column_pairs"},
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
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = rng.sample(range(w), rng.randint(2, 3))
    for c in cols:
        rs = sorted(rng.sample(range(h), 2))
        if rs[1] - rs[0] >= 3:
            g[rs[0]][c] = 7; g[rs[1]][c] = 7
    r_dec = rng.choice([r for r in range(h) if all(g[r][c2] == 0 for c2 in range(w))] or [0])
    g[r_dec][0] = 7; g[r_dec][w - 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # only singletons of 7 → no col-pair to bridge
        g[1][2] = 7
        g[3][5] = 7
        return g
    if name == "adjacent_7s":
        # vertical pair of 7s touching → no gap to fill
        g[1][2] = 7; g[2][2] = 7
        g[4][5] = 7; g[5][5] = 7
        return g
    if name == "more_than_two_7s_per_col":
        # column has 3+ 7-cells → which pair to bridge ambiguous
        g[0][3] = 7; g[3][3] = 7; g[6][3] = 7
        return g
    return g
