"""Generator for arc_additional_puzzles_21_set21_bundle:E145.

Rule: each color with exactly 3 cells at 3 corners of a rectangle
(missing the 4th) → paint the 4th corner that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, missing_corner,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_2_corners, all_4_corners, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "14042d4b8317"
VERSION = "1.1.0"
TASK_ID = "14042d4b8317"
SUMMARY = "1-2 colors with exactly 3 cells at 3 corners of a non-trivial rectangle."

INVARIANTS = [
    "≥1 color with exactly 3 cells at 3 corners of an h×w rect (h,w ≥3)",
    "missing corner is empty (0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_2_corners", "all_4_corners", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "missing_corner": {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rect_corners",
                       "valid": "rect_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    r1 = rng.randint(0, h - 5); r2 = rng.randint(r1 + 3, h - 1)
    c1 = rng.randint(0, w - 5); c2 = rng.randint(c1 + 3, w - 1)
    corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
    missing_idx = rng.randint(0, 3)
    for i, (r, c) in enumerate(corners):
        if i != missing_idx:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "only_2_corners":
        # only 2 same-color corners → 4th corner not derivable
        g[1][1] = 4
        g[5][6] = 4
        return g
    if name == "all_4_corners":
        # all 4 corners present → no missing corner, rule is identity
        for r, c in [(1, 1), (1, 6), (5, 1), (5, 6)]: g[r][c] = 4
        return g
    if name == "collinear_corners":
        # 3 cells on same row → no rectangle defined, cannot infer 4th
        g[3][1] = 4; g[3][4] = 4; g[3][7] = 4
        return g
    return g
