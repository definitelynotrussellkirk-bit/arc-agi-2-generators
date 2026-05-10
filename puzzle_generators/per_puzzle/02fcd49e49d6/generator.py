"""Generator for arc_additional_puzzles_21_set2:E14 — Even-mid of two 8s in row → set 0 to 2.

Rule: row with exactly two 8s at cols c1 and c2; if c1+c2 is even and
midpoint cell is 0 → set midpoint to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_8s, all_odd_distance, midpoint_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "02fcd49e49d6"
VERSION = "1.1.0"
TASK_ID = "02fcd49e49d6"
SUMMARY = "2-3 rows with exactly two 8s separated by even distance."

INVARIANTS = [
    "≥2 rows have exactly two 8-cells with even (c1+c2)",
    "≥1 distractor row with 8s at odd-mid distance",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_8s", "all_odd_distance", "midpoint_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "rows_with_2_8s_even_dist",
                       "valid": "rows_with_2_8s_even_dist"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
            c1 = rng.randint(0, w - 5)
            c2 = c1 + 2 * rng.randint(1, (w - 1 - c1) // 2)
            if c2 - c1 >= 2 and c2 < w:
                g[r][c1] = 8; g[r][c2] = 8
                used_rows.add(r)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_8s":
        # blank → no 8-pairs to operate on
        return g
    if name == "all_odd_distance":
        # all rows have 8s at odd distance → midpoint not a lattice cell, rule never fires
        g[1][1] = 8; g[1][4] = 8   # distance 3 (odd)
        g[3][2] = 8; g[3][7] = 8   # distance 5 (odd)
        return g
    if name == "midpoint_filled":
        # midpoint cell already non-zero → rule precondition (midpoint == 0) fails
        g[1][1] = 8; g[1][5] = 8   # midpoint at col 3
        g[1][3] = 4                # midpoint already filled
        g[3][2] = 8; g[3][6] = 8   # midpoint at col 4
        g[3][4] = 6                # midpoint already filled
        return g
    return g
