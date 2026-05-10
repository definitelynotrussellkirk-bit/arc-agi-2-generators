"""Generator for arc_additional_puzzle_bank_volume2:H10 — Mark intersections of row-0 (1) and col-0 (2).

Rule:
  - cols1 = cols where row 0 has color 1
  - rows2 = rows where col 0 has color 2
  - Output: empty grid with (r, c) painted 3 for every (r, c) in rows2 × cols1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_row_marks,
n_col_marks, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_row_marks, no_col_marks, marker_color_swap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "44756e464c2d"
VERSION = "1.1.0"
TASK_ID = "44756e464c2d"
SUMMARY = "Color-1 markers in row 0; color-2 markers in col 0; output paints intersections with 3."

INVARIANTS = [
    "between 1 and 4 color-1 cells in row 0",
    "between 1 and 4 color-2 cells in col 0",
    "(0,0) stays 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_row_marks", "no_col_marks", "marker_color_swap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_row_marks":    {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "n_col_marks":    {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "row0_col0_markers",
                       "valid": "row0_col0_markers"},
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
        n_row = ctx.draw_int("n_row_marks", 1, min(2, w - 1))
        n_col = ctx.draw_int("n_col_marks", 1, min(2, h - 1))
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_row = ctx.draw_int("n_row_marks", 3, min(4, w - 1))
        n_col = ctx.draw_int("n_col_marks", 3, min(4, h - 1))
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
        n_row = ctx.draw_int("n_row_marks", 1, min(4, w - 1))
        n_col = ctx.draw_int("n_col_marks", 1, min(4, h - 1))
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("placement")
    cols = list(range(1, w)); rng.shuffle(cols)
    for c in cols[:n_row]: g[0][c] = 1
    rows = list(range(1, h)); rng.shuffle(rows)
    for r in rows[:n_col]: g[r][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_row_marks":
        # only col-2 markers → no col selection, no intersections, output has no 3s
        for r in [2, 4, 6]: g[r][0] = 2
        return g
    if name == "no_col_marks":
        # only row-1 markers → no row selection, no intersections, output has no 3s
        for c in [2, 4, 6]: g[0][c] = 1
        return g
    if name == "marker_color_swap":
        # row 0 uses 2 instead of 1; col 0 uses 1 instead of 2 → roles swapped, predicate fails
        for c in [2, 5]: g[0][c] = 2
        for r in [3, 6]: g[r][0] = 1
        return g
    return g
