"""Generator for arc_additional_puzzles_21_set15_bundle:E102 — Frame outline for each color's bbox.

Rule: for each non-bg color, paint frame outline of its bbox in same
color on a fresh empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_cell_colors, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "64592477ccc8"
VERSION = "1.1.0"
TASK_ID = "64592477ccc8"
SUMMARY = "2-3 colors each with 2 cells forming non-degenerate bboxes."

INVARIANTS = [
    "≥2 distinct non-bg colors",
    "each color has 2 cells with bbox spanning ≥2 rows AND ≥2 cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_cell_colors", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "diagonal_color_pairs",
                       "valid": "diagonal_color_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_colors)
    used = set()
    for color in pal:
        for _ in range(20):
            r1 = rng.randint(0, h - 3); r2 = rng.randint(r1 + 2, h - 1)
            c1 = rng.randint(0, w - 3); c2 = rng.randint(c1 + 2, w - 1)
            if (r1, c1) not in used and (r2, c2) not in used and g[r1][c1] == 0 and g[r2][c2] == 0:
                g[r1][c1] = color; g[r2][c2] = color
                used.add((r1, c1)); used.add((r2, c2))
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no bboxes to outline
        return g
    if name == "single_cell_colors":
        # each color appears once → bbox is a single cell, no outline
        g[1][1] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    if name == "collinear_pair":
        # 2 cells on same row/col → bbox collapses to a line, not a frame
        g[2][1] = 4; g[2][8] = 4   # same row
        g[1][5] = 6; g[5][5] = 6   # same col
        return g
    return g
