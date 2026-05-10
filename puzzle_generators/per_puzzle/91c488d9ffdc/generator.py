"""Generator for set5:E30: draw rectangle borders from opposite corners.

Rule: each color appears at two opposite rectangle corners; the rule
draws the border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_cell_colors, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "91c488d9ffdc"
VERSION = "1.1.0"
TASK_ID = "91c488d9ffdc"
SUMMARY = "Each color appears at two opposite rectangle corners; the rule draws the border."
INVARIANTS = ["each used color appears exactly twice", "corner pairs form nondegenerate rectangles", "background is zero"]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_cell_colors", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "diagonal_corners",
                       "valid": "diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_rects", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n_rects", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 12)
        n = ctx.draw_int("n_rects", 1, 3)
    rng = ctx.draw_rng("layout")
    colors = list(ctx.draw_distinct_colors("colors", n=n, exclude={0}))
    g = full_grid(h, w, 0)
    used = set()
    for color in colors:
        for _ in range(50):
            r1 = rng.randint(0, h - 3)
            r2 = rng.randint(r1 + 2, h - 1)
            c1 = rng.randint(0, w - 3)
            c2 = rng.randint(c1 + 2, w - 1)
            pair = {(r1, c1), (r2, c2)}
            if pair & used:
                continue
            for r, c in pair:
                g[r][c] = color
            used |= pair
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no opposite-corner cells defined
        return g
    if name == "single_cell_colors":
        # each color appears once → no opposite corner to pair with
        g[1][1] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    if name == "collinear_corners":
        # 2-cell pair on the same row OR column → rectangle collapses to a line
        g[2][1] = 4; g[2][8] = 4   # same row
        g[1][5] = 6; g[6][5] = 6   # same column
        return g
    return g
