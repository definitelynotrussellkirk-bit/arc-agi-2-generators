"""Generator for arc_puzzle_bank_tenth21:M70 — overlap of two border bboxes → 8.

Rule: two colored rectangular borders overlap. The rule outputs the
filled overlap of their bounding rectangles in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_borders,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, no_green, disjoint_borders.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "600284beb8e4"
VERSION = "1.1.0"
TASK_ID = "600284beb8e4"
SUMMARY = "Color-2 and color-3 border rectangles define an overlap mask."

INVARIANTS = [
    "there is one color-2 rectangular border",
    "there is one color-3 rectangular border",
    "the two border bounding boxes have a non-empty intersection",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "no_green", "disjoint_borders")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_borders":      {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_overlapping_borders",
                       "valid": "two_overlapping_borders"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_border(g, top, left, bottom, right, color):
    for c in range(left, right + 1):
        g[top][c] = color
        g[bottom][c] = color
    for r in range(top, bottom + 1):
        g[r][left] = color
        g[r][right] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    top2 = 1
    left2 = rng.randint(1, 2)
    bottom2 = h - 3
    right2 = w - 4
    top3 = rng.randint(2, min(3, bottom2))
    left3 = rng.randint(max(left2 + 2, right2 - 2), right2)
    bottom3 = h - 2
    right3 = w - 2
    _draw_border(g, top2, left2, bottom2, right2, 2)
    _draw_border(g, top3, left3, bottom3, right3, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_red":
        # only color-3 border → no red bbox to intersect with
        _draw_border(g, 2, 4, 7, 9, 3)
        return g
    if name == "no_green":
        # only color-2 border → no green bbox to intersect with
        _draw_border(g, 1, 1, 6, 6, 2)
        return g
    if name == "disjoint_borders":
        # both borders exist but bounding boxes don't overlap → empty intersection
        _draw_border(g, 1, 1, 3, 3, 2)
        _draw_border(g, 5, 6, 7, 9, 3)
        return g
    return g
