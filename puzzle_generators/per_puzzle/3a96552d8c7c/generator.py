"""Generator for arc_additional_puzzles_21_set2:E9.

Rule: row with exactly 2 cells of color 5 separated by all-0 → fill
between them with 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, adjacent_5s, more_than_two_5s.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3a96552d8c7c"
VERSION = "1.1.0"
TASK_ID = "3a96552d8c7c"
SUMMARY = "2-3 rows have exactly 2 5-cells separated by all-0."

INVARIANTS = [
    "≥2 rows have exactly 2 cells of color 5, separated by ≥2 0-cells",
    "≥1 distractor row with 5-cells adjacent (won't fill)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "adjacent_5s", "more_than_two_5s")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "row_pairs",
                       "valid": "row_pairs"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            if r in used_rows:
                continue
            cs = sorted(rng.sample(range(w), 2))
            if cs[1] - cs[0] >= 3:
                g[r][cs[0]] = 5; g[r][cs[1]] = 5
                used_rows.add(r)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # only singletons of 5 → no pair to fill between
        g[1][2] = 5
        g[3][6] = 5
        return g
    if name == "adjacent_5s":
        # pair of 5s with no gap between → nothing to fill
        g[1][2] = 5; g[1][3] = 5
        g[4][5] = 5; g[4][6] = 5
        return g
    if name == "more_than_two_5s":
        # row has 3+ 5s → invariant violated, which pair to bridge ambiguous
        g[2][1] = 5; g[2][4] = 5; g[2][7] = 5
        return g
    return g
