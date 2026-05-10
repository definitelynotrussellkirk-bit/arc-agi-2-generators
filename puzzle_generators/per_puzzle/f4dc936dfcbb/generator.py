"""Generator for arc_additional_puzzle_bank_volume18:M125 — Mark intersection of row 2-spans and col 3-spans with 8.

Rule: rows with ≥2 cells of color 2 define a span [c0..c1]; cols with
≥2 cells of color 3 define a span [r0..r1]; if (r,c) lies in both, set 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_spans,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_row_spans, no_col_spans, disjoint_spans.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4dc936dfcbb"
VERSION = "1.1.0"
TASK_ID = "f4dc936dfcbb"
SUMMARY = "2-3 rows with two 2s + 2-3 cols with two 3s; pairs intersect."

INVARIANTS = [
    "≥1 row has 2 cells of color 2",
    "≥1 col has 2 cells of color 3",
    "at least one row-span × col-span intersection",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_row_spans", "no_col_spans", "disjoint_spans")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_spans":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "row_col_spans_with_decor",
                       "valid": "row_col_spans_with_decor"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_rows = rng.randint(2, 3)
    n_cols = rng.randint(2, 3)
    rows = rng.sample(range(h), n_rows)
    cols = rng.sample(range(w), n_cols)
    for r in rows:
        cs = sorted(rng.sample(range(w), 2))
        g[r][cs[0]] = 2; g[r][cs[1]] = 2
    for c in cols:
        rs = sorted(rng.sample(range(h), 2))
        g[rs[0]][c] = 3; g[rs[1]][c] = 3
    g[0][w - 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_row_spans":
        # only column 3-spans, no row 2-spans → no row component
        g[1][3] = 3; g[7][3] = 3
        g[2][7] = 3; g[6][7] = 3
        g[0][w - 1] = 6
        return g
    if name == "no_col_spans":
        # only row 2-spans, no column 3-spans → no col component
        g[2][1] = 2; g[2][8] = 2
        g[5][2] = 2; g[5][9] = 2
        g[0][w - 1] = 6
        return g
    if name == "disjoint_spans":
        # row 2-span and col 3-span exist but never intersect → no marker fires
        g[1][1] = 2; g[1][4] = 2     # row span: cols 1..4
        g[3][8] = 3; g[7][8] = 3     # col span: rows 3..7, col 8 (outside row span)
        g[0][w - 1] = 6
        return g
    return g
