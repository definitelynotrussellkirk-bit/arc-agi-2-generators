"""Generator for arc_additional_puzzles_21_set6:E42 — Each color → 4 cells at corners of its bbox.

Rule: for each non-bg color, compute bbox of its cells; emit 4 corner
cells of that bbox in that color on a fresh empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_colors, single_cell_color, bbox_too_small.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "47993d3762b9"
VERSION = "1.1.0"
TASK_ID = "47993d3762b9"
SUMMARY = "Scattered cells in 2-3 colors, each with bbox spanning ≥3×3."

INVARIANTS = [
    "≥2 distinct non-bg colors",
    "each color has bbox spanning ≥3 rows AND ≥3 cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_colors", "single_cell_color", "bbox_too_small")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "scattered_with_large_bbox",
                       "valid": "scattered_with_large_bbox"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_colors)
    for color in pal:
        for _ in range(20):
            r1 = rng.randint(0, h - 4); r2 = rng.randint(r1 + 3, h - 1)
            c1 = rng.randint(0, w - 4); c2 = rng.randint(c1 + 3, w - 1)
            if g[r1][c1] == 0 and g[r2][c2] == 0:
                g[r1][c1] = color; g[r2][c2] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_colors":
        # blank → no colors to compute bboxes for
        return g
    if name == "single_cell_color":
        # color has only 1 cell → bbox is 1x1, no 4-corner output (or trivial)
        g[3][4] = 4
        g[1][1] = 6; g[5][7] = 6   # 6 has proper bbox
        return g
    if name == "bbox_too_small":
        # bboxes <3×3 → corners coincide / degenerate
        g[1][1] = 4; g[2][2] = 4   # 2x2 bbox
        g[5][3] = 6; g[5][5] = 6   # 1-row bbox (height 1)
        return g
    return g
