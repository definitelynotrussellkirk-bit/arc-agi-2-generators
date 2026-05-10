"""Generator for arc_additional_puzzles_21_set4:E23 — Connect 2-cell pairs of color 1 within each row.

Rule: each row with exactly 2 cells of color 1 → fill all cells between
them (inclusive) with 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_paired_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_singletons, three_in_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dff6bf5f78ab"
VERSION = "1.1.0"
TASK_ID = "dff6bf5f78ab"
SUMMARY = "2-3 rows have exactly 2 1-cells, plus 1 distractor row with 1 isolated 1-cell."

INVARIANTS = [
    "≥2 rows have exactly 2 cells of color 1, separated by ≥1 0-cell",
    "≥1 distractor row has only 1 cell of color 1 (won't trigger)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_singletons", "three_in_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_paired_rows":  {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "row_pairs_with_distractor",
                       "valid": "row_pairs_with_distractor"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        w = ctx.draw_int("grid_w", 8, 8)
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
            if cs[1] - cs[0] >= 2:
                g[r][cs[0]] = 1; g[r][cs[1]] = 1
                used_rows.add(r)
                break
    for _ in range(20):
        r = rng.randint(0, h - 1)
        if r not in used_rows:
            g[r][rng.randint(0, w - 1)] = 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no rows with pairs, rule has no effect
        return g
    if name == "single_singletons":
        # every row has only 1 cell → predicate "exactly 2" never true, rule is identity
        g[1][3] = 1
        g[3][5] = 1
        g[5][2] = 1
        return g
    if name == "three_in_row":
        # rows with 3 1-cells → predicate "exactly 2" fails, rule has no effect
        g[1][1] = 1; g[1][3] = 1; g[1][7] = 1
        g[3][2] = 1; g[3][5] = 1; g[3][8] = 1
        return g
    return g
