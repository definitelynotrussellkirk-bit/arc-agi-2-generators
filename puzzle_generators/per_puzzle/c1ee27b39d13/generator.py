"""Generator for arc_puzzle_bank_21_set5_s:S5_H7.

Rule: top markers choose columns and left markers choose rows from the
interior grid; output is the submatrix.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows, n_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_row_markers, no_col_markers, all_marked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c1ee27b39d13"
VERSION = "1.1.0"
TASK_ID = "c1ee27b39d13"
SUMMARY = "Top markers choose columns and left markers choose rows from the interior grid."

INVARIANTS = [
    "background is 0",
    "top row color-4 markers select at least two interior columns",
    "left column color-5 markers select at least two interior rows",
    "selected rows and columns are a proper subset of the interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_row_markers", "no_col_markers", "all_marked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_row_marks":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "border_markers_dense_interior",
                       "valid": "border_markers_dense_interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sel_rows = sorted(rng.sample(range(1, h), rng.randint(2, min(4, h - 2))))
    sel_cols = sorted(rng.sample(range(1, w), rng.randint(2, min(4, w - 2))))
    for r in sel_rows:
        g[r][0] = 5
    for c in sel_cols:
        g[0][c] = 4
    colors = [1, 2, 3, 6, 7, 8, 9]
    for r in range(1, h):
        for c in range(1, w):
            g[r][c] = rng.choice(colors + [0, 0])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 6, 7, 8, 9]
    for r in range(1, h):
        for c in range(1, w):
            g[r][c] = colors[(r + c) % len(colors)]
    if name == "no_row_markers":
        # only column markers → no row selection, submatrix collapses
        for c in [2, 5]: g[0][c] = 4
        return g
    if name == "no_col_markers":
        # only row markers → no column selection, submatrix collapses
        for r in [2, 5]: g[r][0] = 5
        return g
    if name == "all_marked":
        # every interior row and column marked → submatrix == interior (rule is identity)
        for r in range(1, h): g[r][0] = 5
        for c in range(1, w): g[0][c] = 4
        return g
    return g
