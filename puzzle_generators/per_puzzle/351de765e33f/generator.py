"""Generator for arc_additional_puzzle_bank_volume2:M8.

Rule: the second-largest object, after reading-order tie breaks, is
recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, two_objects, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "351de765e33f"
VERSION = "1.1.0"
TASK_ID = "351de765e33f"
SUMMARY = "The second-largest object, after reading-order tie breaks, is recolored to 8."

INVARIANTS = [
    "at least three separated nonzero objects are present",
    "object sizes are distinct so the second-largest choice is unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "two_objects", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "size_spread":    {"type": "str", "default": "5_3_2", "valid": "5_3_2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_cells(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0, 8]))
    g = full_grid(h, w, 0)
    _draw_cells(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], colors[0])
    _draw_cells(g, h - 4, w - 4, [(0, 0), (0, 1), (1, 0)], colors[1])
    _draw_cells(g, 1, w - 3, [(0, 0), (1, 0)], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "equal_sizes":
        # 3 objects all the same size → "second largest" is ambiguous
        sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
        _draw_cells(g, 1, 1, sq, 4)
        _draw_cells(g, 1, w - 3, sq, 6)
        _draw_cells(g, h - 3, 4, sq, 7)
        return g
    if name == "two_objects":
        # only 2 objects → "second largest" coincides with smallest
        _draw_cells(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 4)
        _draw_cells(g, h - 4, w - 4, [(0, 0), (0, 1), (1, 0)], 6)
        return g
    if name == "single_object":
        # 1 object → no "second" exists at all
        _draw_cells(g, 3, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 4)
        return g
    return g
