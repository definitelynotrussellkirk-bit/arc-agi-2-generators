"""Generator for v3_rich_schema:hard_07_fill_ring_by_repeated_corner_color.

Rule: fill green ring interiors with the corner color that repeats most.

Combinatorial axes (8): grid_h, grid_w, palette_kind, fill_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_corners_unique, no_rings, all_corners_same.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "11221f58af4b"
VERSION = "1.1.0"
TASK_ID = "11221f58af4b"
SUMMARY = "Fill green ring interiors with the corner color that repeats most."

INVARIANTS = [
    "the four grid corners contain marker colors",
    "one corner color appears at least twice and is the fill color",
    "there are one or more hollow color-3 rectangular rings",
    "ring borders and corner markers are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_corners_unique", "no_rings", "all_corners_same")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "fill_color":     {"type": "int", "default": "rng choice", "valid": "1..9 except 3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "corners_plus_rings",
                       "valid": "corners_plus_rings"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "rings", "valid": "rings"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _ring(g, top, left, h, w):
    for c in range(left, left + w):
        g[top][c] = 3
        g[top + h - 1][c] = 3
    for r in range(top, top + h):
        g[r][left] = 3
        g[r][left + w - 1] = 3


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        fill = ctx.draw_choice("fill_color", [1, 2, 4, 5])
    elif difficulty == "hard":
        fill = ctx.draw_choice("fill_color", [6, 7, 8, 9])
    else:
        fill = ctx.draw_choice("fill_color", [1, 2, 4, 5, 6, 7, 8, 9])
    other = rng.choice([c for c in [1, 2, 4, 5, 6, 7, 8, 9] if c != fill])
    g = full_grid(10, 12, 0)
    g[0][0] = fill
    g[0][11] = fill
    g[9][0] = fill
    g[9][11] = other
    _ring(g, 2, 2, 5, 4)
    _ring(g, 3, 8, 5, 3)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "all_corners_unique":
        # all 4 corners distinct → no repeated color, fill is undefined
        g[0][0] = 1; g[0][11] = 2; g[9][0] = 4; g[9][11] = 6
        _ring(g, 2, 2, 5, 4)
        _ring(g, 3, 8, 5, 3)
        return g
    if name == "no_rings":
        # corners but no rings → nothing to fill
        g[0][0] = 4; g[0][11] = 4; g[9][0] = 4; g[9][11] = 6
        return g
    if name == "all_corners_same":
        # all 4 corners identical → fill is unambiguous but maximal
        g[0][0] = 4; g[0][11] = 4; g[9][0] = 4; g[9][11] = 4
        _ring(g, 2, 2, 5, 4)
        _ring(g, 3, 8, 5, 3)
        return g
    return g
