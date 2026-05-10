"""Generator for arc_puzzle_bank_21_set16_s:S16_M7.

Rule: one cell of color 1 (shared corner), one cell of color 2 (other-h
corner — same row as 1), one cell of color 3 (other-v corner — same
col as 1). Output draws the rectangle outline (bbox border) in 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rect_dims,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_color_1, missing_color_2_or_3, collinear_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1acd7639146e"
VERSION = "1.1.0"
TASK_ID = "1acd7639146e"
SUMMARY = "Three markers: 1=shared corner, 2=horizontal-axis other corner, 3=vertical-axis other corner."

INVARIANTS = [
    "background is 0",
    "exactly one cell of each of colors 1, 2, 3",
    "row(1) == row(2) and col(1) == col(3)",
    "the rectangle is at least 3×3 (so outline is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_color_1", "missing_color_2_or_3", "collinear_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_dims":      {"type": "str", "default": "rng span ≥3", "valid": "≥3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "L_shape_markers",
                       "valid": "L_shape_markers"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1 = rng.randint(1, h - 4)
    c1 = rng.randint(1, w - 4)
    c2 = rng.randint(c1 + 3, w - 1)
    r2 = rng.randint(r1 + 3, h - 1)
    g[r1][c1] = 1
    g[r1][c2] = 2
    g[r2][c1] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "missing_color_1":
        # no shared-corner marker → rectangle is undefined (no anchor)
        g[1][6] = 2
        g[5][1] = 3
        return g
    if name == "missing_color_2_or_3":
        # only 2 of 3 markers → 4th corner not derivable
        g[1][1] = 1
        g[1][6] = 2
        return g
    if name == "collinear_markers":
        # all three markers on the same row → no rectangle possible
        g[3][1] = 1
        g[3][4] = 2
        g[3][7] = 3
        return g
    return g
