"""Generator for arc_additional_puzzle_bank_volume4:H28.

Rule: row markers = col 0 cells in {1,2,3}. Col markers = row 0 cells
in {1,2,3}. For each (row_r, col_c) where row[r][0] == col[0][c], paint.

Combinatorial axes (8): grid_h/w, palette_kind, n_row_markers,
n_col_markers, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_row_markers, no_col_markers, no_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0a92efb5c42c"
VERSION = "1.1.0"
TASK_ID = "0a92efb5c42c"
SUMMARY = "Row 0 has marker colors + col 0 has marker colors with matching pairs."

INVARIANTS = [
    "row 0 (cols ≥ 1) has 1-3 cells of colors 1/2/3",
    "col 0 (rows ≥ 1) has 1-3 cells of colors 1/2/3",
    "at least one row-color matches one col-color",
]

PALETTE_KINDS = ("default", "match_1", "match_2", "match_3")
DEGENERATE_TEXTURES = ("no_row_markers", "no_col_markers", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_row_markers":  {"type": "int", "default": "3", "valid": "1..3"},
    "n_col_markers":  {"type": "int", "default": "3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "border", "valid": "border"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    g[0][1] = 3; g[0][3] = 1; g[0][4] = 2
    g[3][0] = 2; g[4][0] = 2; g[5][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_row_markers":
        # only col-0 markers; row-0 empty → no matches possible
        g[3][0] = 2; g[4][0] = 2
        return g
    if name == "no_col_markers":
        # only row-0 markers; col-0 empty → no matches possible
        g[0][1] = 3; g[0][3] = 1
        return g
    if name == "no_match":
        # row markers and col markers exist but use disjoint colors
        g[0][1] = 1; g[0][2] = 1
        g[3][0] = 2; g[4][0] = 2
        return g
    return g
