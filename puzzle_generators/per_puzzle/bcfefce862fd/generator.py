"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_128_fill_rectangle_from_opposite_corners.

Rule: two same-color opposite corner markers define a filled rectangle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rect_dims,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: collinear_markers, single_marker, mismatched_marker_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bcfefce862fd"
VERSION = "1.1.0"
TASK_ID = "bcfefce862fd"
SUMMARY = "Two same-color opposite corner markers define a filled rectangle."

INVARIANTS = [
    "background is 0",
    "exactly two nonzero cells are present",
    "the two markers share one color",
    "markers are opposite corners of a rectangle with positive area",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("collinear_markers", "single_marker", "mismatched_marker_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_dims":      {"type": "str", "default": "rng span ≥3", "valid": "≥3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "diagonal_corners",
                       "valid": "diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1 = rng.randint(0, h - 4)
    r2 = rng.randint(r1 + 2, h - 1)
    c1 = rng.randint(0, w - 4)
    c2 = rng.randint(c1 + 2, w - 1)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if rng.randrange(2) == 0:
        g[r1][c1] = color
        g[r2][c2] = color
    else:
        g[r1][c2] = color
        g[r2][c1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "collinear_markers":
        # markers in same row → degenerate "rectangle" is a line, zero area
        g[2][2] = 4
        g[2][7] = 4
        return g
    if name == "single_marker":
        # only one marker → no opposite corner, rectangle undefined
        g[2][3] = 4
        return g
    if name == "mismatched_marker_colors":
        # two markers of different colors → rule requires same color, no match
        g[1][1] = 4
        g[5][7] = 6
        return g
    return g
