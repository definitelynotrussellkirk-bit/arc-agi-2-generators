"""Generator for arc_additional_puzzle_bank_volume13:H90.

Rule: blue objects with normalized shapes appearing an odd number of
times are recolored to 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_odd, n_even,
palette_size, position_bias, n_distinct_colors, shape_kind, texture.
Degenerates: no_odd_shape, all_odd, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "529337742c5c"
VERSION = "1.1.0"
TASK_ID = "529337742c5c"
SUMMARY = "Blue objects with normalized shapes appearing an odd number of times are recolored to 2."

INVARIANTS = [
    "all relevant components are color 1",
    "one normalized shape appears three times and another appears two times",
]

PALETTE_KINDS = ("default", "L_pair", "T_pair", "Z_pair")
DEGENERATE_TEXTURES = ("no_odd_shape", "all_odd", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_odd":          {"type": "int", "default": "3", "valid": "3"},
    "n_even":         {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "shape_kind":     {"type": "str", "default": "L_T", "valid": "L_T"},
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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 12, 15)
    g = full_grid(h, w, 0)
    odd_shape = [(0, 0), (1, 0), (1, 1)]
    even_shape = [(0, 0), (0, 1), (1, 1)]
    placements = [
        (1, 1, odd_shape),
        (1, w - 4, odd_shape),
        (h - 4, 1, odd_shape),
        (h - 4, w - 4, even_shape),
        (h // 2, w // 2, even_shape),
    ]
    for top, left, cells in placements:
        paint_at(g, top, left, cells, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    odd_shape = [(0, 0), (1, 0), (1, 1)]
    even_shape = [(0, 0), (0, 1), (1, 1)]
    if name == "no_odd_shape":
        # all shapes appear an even number of times → no recolor target
        for top, left, cells in [(1, 1, odd_shape), (1, w - 4, odd_shape),
                                  (h - 4, 1, even_shape), (h - 4, w - 4, even_shape)]:
            paint_at(g, top, left, cells, 1)
        return g
    if name == "all_odd":
        # every shape appears odd-count → output recolors everything to 2
        for top, left, cells in [(1, 1, odd_shape), (1, w - 4, odd_shape),
                                  (h - 4, 1, odd_shape), (h - 4, w - 4, even_shape)]:
            paint_at(g, top, left, cells, 1)
        return g
    if name == "no_blobs":
        # empty grid — no shapes to count, rule produces an empty result
        return g
    return g
