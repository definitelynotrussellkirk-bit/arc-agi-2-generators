"""Generator for arc_additional_puzzle_bank_volume15:M100 — Mark intersections of color-1 row markers and color-2 col markers in row 0.

Rule:
  - mark-rows = rows of all color-1 cells (anywhere in grid)
  - mark-cols = cols of color-2 cells in row 0
  - Output: paint (r, c) for r in rows × c in cols with color 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_row_marks,
n_col_marks, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_row_marks, no_col_marks, marks_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ff973026bfbe"
VERSION = "1.1.0"
TASK_ID = "ff973026bfbe"
SUMMARY = "Color-1 cells (anywhere) and color-2 cells in row 0; output paints intersections with 3."

INVARIANTS = [
    "1..3 color-1 cells, each in a distinct row",
    "1..3 color-2 cells in row 0",
    "color-1 cells aren't in row 0 (else they'd be ambiguous)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_row_marks", "no_col_marks", "marks_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_row_marks":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "n_col_marks":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "row_and_col_markers",
                       "valid": "row_and_col_markers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n_row = ctx.draw_int("n_row_marks", 1, 2)
        n_col = ctx.draw_int("n_col_marks", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_row = ctx.draw_int("n_row_marks", 3, 3)
        n_col = ctx.draw_int("n_col_marks", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
        n_row = ctx.draw_int("n_row_marks", 1, 3)
        n_col = ctx.draw_int("n_col_marks", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    rows = list(range(1, h))
    rng.shuffle(rows)
    for r in rows[:n_row]:
        c = rng.randint(0, w - 1)
        g[r][c] = 1
    cols = list(range(0, w))
    rng.shuffle(cols)
    for c in cols[:n_col]:
        g[0][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_row_marks":
        # no color-1 cells → no rows to mark, rule fires zero times
        g[0][2] = 2; g[0][5] = 2
        return g
    if name == "no_col_marks":
        # no color-2 in row 0 → no cols to mark, rule fires zero times
        g[2][3] = 1; g[5][6] = 1; g[6][1] = 1
        return g
    if name == "marks_overlap":
        # color-1 IS in row 0 → ambiguous: is it a row marker or a non-marker stray?
        g[0][2] = 1   # color-1 in row 0 violates the disambiguation
        g[0][5] = 2
        g[3][4] = 1; g[6][7] = 1
        return g
    return g
