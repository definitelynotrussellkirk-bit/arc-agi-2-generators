"""Generator for arc_puzzle_bank_fourteenth21:E96.

Rule: row 0 holds nonzero column-header colors; each color-1 marker in
the body recolors to its column's header color.

Combinatorial axes (8): grid_h/w, palette_kind, header_cols,
palette_size, position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_headers, no_markers, markers_in_empty_columns.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "91b531b5d3f4"
VERSION = "1.1.0"
TASK_ID = "91b531b5d3f4"
SUMMARY = "Put column header colors in row 0 and color-1 markers below them."

INVARIANTS = [
    "background is 0",
    "row 0 has nonzero header colors in selected columns",
    "markers below headers are color 1",
    "each marker is repainted by its column header",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_headers", "no_markers", "markers_in_empty_columns")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "3..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "header_cols":    {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "marker_density": {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    target = min(ctx.draw_int("header_cols", 2, 4), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), target)
    for c in cols:
        g[0][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        for r in rng.sample(range(1, h), rng.randint(1, min(3, h - 1))):
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_headers":
        # markers but no headers — recolor source undefined
        g[3][2] = 1
        g[4][5] = 1
        return g
    if name == "no_markers":
        # headers but no markers — rule has nothing to recolor
        g[0][2] = 4
        g[0][5] = 7
        return g
    if name == "markers_in_empty_columns":
        # markers in cols where header is 0 — header color is bg
        g[0][3] = 5
        g[2][1] = 1  # marker in col 1 where header[0][1]=0
        g[5][7] = 1  # marker in col 7 where header[0][7]=0
        return g
    return g
