"""Generator for 21b:m142 — fill header selected intersections.

Rule: top-row markers (color 2) at certain columns + left-col markers
(color 3) at certain rows. At every (row, col) intersection of (left
3, top 2), place a 5. Cell (0,0) holds an unrelated 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_top, n_left,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_markers, no_left_markers, missing_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0be8ff9b4144"
VERSION = "1.1.0"
TASK_ID = "0be8ff9b4144"
SUMMARY = "8 anchor at (0,0) + top-row 2-markers + left-col 3-markers."

INVARIANTS = [
    "background is 0",
    "cell (0,0) is 8",
    "row 0 cols 1.. has 2-3 cells of color 2",
    "col 0 rows 1.. has 2-3 cells of color 3",
    "interior cells are bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_markers", "no_left_markers", "missing_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_top":          {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n_left":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "header_with_markers",
                       "valid": "header_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
        n_top = 2
        n_left = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_top = 3
        n_left = 3
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        n_top = ctx.draw_int("n_top", 2, 3)
        n_left = ctx.draw_int("n_left", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = 8
    top_cols = rng.sample(range(1, w), n_top)
    for c in top_cols: g[0][c] = 2
    left_rows = rng.sample(range(1, h), n_left)
    for r in left_rows: g[r][0] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    g[0][0] = 8
    if name == "no_top_markers":
        # only left-col markers, no top → no intersections, output has no 5s
        for r in [2, 4, 6]: g[r][0] = 3
        return g
    if name == "no_left_markers":
        # only top-row markers, no left → no intersections, output has no 5s
        for c in [2, 5, 7]: g[0][c] = 2
        return g
    if name == "missing_anchor":
        # (0,0) anchor missing → header convention violated, ambiguous parse
        g[0][0] = 0
        for c in [2, 5]: g[0][c] = 2
        for r in [3, 6]: g[r][0] = 3
        return g
    return g
