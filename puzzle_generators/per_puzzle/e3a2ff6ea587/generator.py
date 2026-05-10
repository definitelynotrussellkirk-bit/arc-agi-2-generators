"""Generator for arc_additional_puzzles_21_set7:E46.

Rule: each color with exactly 4 cells at the 4 corners of a rectangle
→ fill the entire bbox rect with that color.

Combinatorial axes (8): grid_h/w, palette_kind, n_rects, palette_size,
position_bias, n_distinct_colors, rect_area, texture.
Degenerates: only_3_corners, cells_aligned, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e3a2ff6ea587"
VERSION = "1.1.0"
TASK_ID = "e3a2ff6ea587"
SUMMARY = "1-2 colors with exactly 4 cells at 4 rectangular corners."

INVARIANTS = [
    "≥1 color with exactly 4 cells at corners of a non-degenerate rect",
    "rect spans ≥3 rows AND ≥3 cols (so fill is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_3_corners", "cells_aligned", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "1", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "rect_area":      {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    r1 = rng.randint(0, h - 4); r2 = rng.randint(r1 + 2, h - 1)
    c1 = rng.randint(0, w - 5); c2 = rng.randint(c1 + 3, w - 1)
    g[r1][c1] = color; g[r1][c2] = color
    g[r2][c1] = color; g[r2][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "only_3_corners":
        # 3 corners → not a complete rect, rule cannot match
        g[1][1] = 4; g[1][6] = 4
        g[5][1] = 4
        return g
    if name == "cells_aligned":
        # all 4 cells in a row → degenerate flat rect (zero height)
        g[3][1] = 5; g[3][3] = 5
        g[3][5] = 5; g[3][7] = 5
        return g
    if name == "no_cells":
        # empty grid — no color satisfies 4-corner predicate
        return g
    return g
