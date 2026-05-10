"""Generator for arc_puzzle_bank_21_set4:S4_M6 — four corners → perimeter.

Rule: each color appearing exactly 4 times at the corners of a
non-degenerate axis-aligned rectangle → draw the rectangle's perimeter
in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, three_corners_only, degenerate_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "863b3767a13c"
VERSION = "1.1.0"
TASK_ID = "863b3767a13c"
SUMMARY = "1-2 colors each at 4 corners of a non-degenerate rectangle."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears at 4 axis-aligned corners",
    "rectangles don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "three_corners_only", "degenerate_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "four_corner_rects",
                       "valid": "four_corner_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    reserved: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 4)
            c1 = rng.randint(0, w - 4)
            r2 = rng.randint(r1 + 3, min(h - 1, r1 + 5))
            c2 = rng.randint(c1 + 3, min(w - 1, c1 + 5))
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & reserved:
                continue
            g[r1][c1] = color; g[r1][c2] = color
            g[r2][c1] = color; g[r2][c2] = color
            reserved |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no corner sets to draw perimeters of
        return g
    if name == "three_corners_only":
        # color appears 3 times → "exactly 4 corners" precondition fails
        g[1][1] = 4
        g[1][7] = 4
        g[5][1] = 4  # missing (5, 7)
        return g
    if name == "degenerate_rect":
        # 4 cells colinear (1 row only) → not a rectangle
        for c in [1, 4, 7, 10]: g[3][c] = 4
        return g
    return g
