"""Generator for arc_puzzle_bank_21_set13_s:S13_M4 — area strip in reading order.

Rule: separated objects are converted to a reading-order strip of their
areas (each cell is colored by area, sorted by top-left position).

Combinatorial axes (8): grid_h, grid_w, palette_kind, include_fourth,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, all_same_area, area_too_large.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "941f7ac13580"
VERSION = "1.1.0"
TASK_ID = "941f7ac13580"
SUMMARY = "Separated objects are converted to a reading-order strip of their areas."

INVARIANTS = [
    "background is 0",
    "every object area fits in one ARC color digit",
    "objects are separated and ordered by top-left position",
    "area values are intentionally visible as output colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "all_same_area", "area_too_large")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "include_fourth": {"type": "bool", "default": "rng", "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "row_aligned_distinct_areas",
                       "valid": "row_aligned_distinct_areas"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

DOT = [(0, 0)]
L_3 = [(0, 0), (1, 0), (1, 1)]
RECT_2X2 = [(r, c) for r in range(2) for c in range(2)]
PLUS_5 = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 12, 13)
        include_fourth = ctx.draw_choice("include_fourth", [False])
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 14, 15)
        include_fourth = ctx.draw_choice("include_fourth", [True])
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 12, 15)
        include_fourth = ctx.draw_choice("include_fourth", [False, True])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r0 = rng.randint(1, 2)
    paint_at(g, r0, 1, DOT, 2)
    paint_at(g, r0, 4, L_3, 3)
    paint_at(g, r0, 8, RECT_2X2, 4)
    if include_fourth:
        paint_at(g, h - 4, w - 4, PLUS_5, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no objects to encode, output strip empty
        return g
    if name == "all_same_area":
        # all 3 objects same size (3) → strip is uniform color (degenerate signal)
        paint_at(g, 1, 1, L_3, 2)
        paint_at(g, 1, 5, L_3, 3)
        paint_at(g, 1, 9, L_3, 4)
        return g
    if name == "area_too_large":
        # object area exceeds 9 (10 cells) → can't fit in one ARC color digit
        big = [(r, c) for r in range(2) for c in range(5)]   # 10 cells
        paint_at(g, 1, 1, big, 2)
        paint_at(g, 5, 1, DOT, 3)
        return g
    return g
