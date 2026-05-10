"""Generator for arc_additional_puzzle_bank_volume12:H83.

Rule: the red shape class with odd frequency up to rotation has each
component bounding box filled orange.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_odd, n_even,
palette_size, position_bias, n_distinct_colors, shape_kind, texture.
Degenerates: no_odd_class, all_odd, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "e14a91c50791"
VERSION = "1.1.0"
TASK_ID = "e14a91c50791"
SUMMARY = "The red shape class with odd frequency up to rotation has each component bounding box filled orange."

INVARIANTS = [
    "all considered components are red",
    "one rotation-equivalent shape class appears an odd number of times",
    "other red shape classes appear an even number of times",
    "odd-class shapes have non-filled bounding boxes",
]

PALETTE_KINDS = ("default", "L_odd", "T_odd", "Z_odd")
DEGENERATE_TEXTURES = ("no_odd_class", "all_odd", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..17", "valid": "10..24"},
    "grid_w":         {"type": "int", "default": "rng 15..20", "valid": "12..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_odd":          {"type": "int", "default": "3", "valid": "3"},
    "n_even":         {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "shape_kind":     {"type": "str", "default": "L_vs_square", "valid": "L_vs_square"},
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
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 17)
        w = ctx.draw_int("grid_w", 18, 20)
    else:
        h = ctx.draw_int("grid_h", 13, 17)
        w = ctx.draw_int("grid_w", 15, 20)
    g = full_grid(h, w, 0)
    odd = [(0, 0), (1, 0), (2, 0), (2, 1)]
    square = [(0, 0), (0, 1), (1, 0), (1, 1)]
    paint_at(g, 1, 1, odd, 2)
    paint_at(g, 1, 8, odd, 2)
    paint_at(g, h - 5, 2, odd, 2)
    paint_at(g, h - 5, w - 5, square, 2)
    paint_at(g, 4, w - 5, square, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 17
    g = full_grid(h, w, 0)
    odd = [(0, 0), (1, 0), (2, 0), (2, 1)]
    square = [(0, 0), (0, 1), (1, 0), (1, 1)]
    if name == "no_odd_class":
        # every shape class appears an even number of times → no class to highlight
        for top, left in [(1, 1), (1, 8)]:
            paint_at(g, top, left, odd, 2)
        for top, left in [(h - 5, w - 5), (4, w - 5)]:
            paint_at(g, top, left, square, 2)
        return g
    if name == "all_odd":
        # both classes appear an odd number of times → ambiguous selection
        paint_at(g, 1, 1, odd, 2)
        paint_at(g, 1, 8, odd, 2)
        paint_at(g, h - 5, 2, odd, 2)
        paint_at(g, h - 5, w - 5, square, 2)
        return g
    if name == "no_blobs":
        # empty grid — no shapes, no class to recolor
        return g
    return g
