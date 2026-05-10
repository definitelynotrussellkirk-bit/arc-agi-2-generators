"""Generator for arc_puzzle_bank_21_set7_s:S7_H2.

Slide all non-wall objects in the direction encoded by the corner header.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_objects, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e09918db7bb"
VERSION = "1.1.0"
TASK_ID = "2e09918db7bb"
SUMMARY = "Slide all non-wall objects in the direction encoded by the corner header."

INVARIANTS = [
    "cell (0,0) is a direction marker",
    "color-8 cells are fixed blockers",
    "other colored objects slide as whole components until blocked",
    "at least one object moves under the selected gravity direction",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_objects", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "marker_plus_walls_plus_objects",
                       "valid": "marker_plus_walls_plus_objects"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_VARIANTS = [
    (4, [(1, 2, [(0, 0), (0, 1), (1, 0)], 5), (2, 8, [(0, 0), (1, 0), (1, 1)], 6)]),
    (4, [(1, 4, [(0, 0), (1, 0), (1, 1)], 2), (3, 8, [(0, 0), (0, 1)], 7)]),
    (2, [(2, 1, [(0, 0), (1, 0), (1, 1)], 3), (5, 2, [(0, 0), (0, 1)], 6)]),
    (1, [(2, 8, [(0, 0), (1, 0), (1, 1)], 4), (5, 7, [(0, 0), (0, 1)], 6)]),
    (3, [(6, 2, [(0, 0), (0, 1), (1, 1)], 5), (6, 8, [(0, 0), (1, 0)], 7)]),
    (4, [(1, 1, [(0, 0), (0, 1)], 2), (2, 9, [(0, 0), (1, 0)], 6)]),
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        idx = ctx.draw_int("variant", 0, 1)
    elif difficulty == "hard":
        idx = ctx.draw_int("variant", 4, 5)
    else:
        idx = ctx.draw_int("variant", 0, 5)
    marker, placements = _VARIANTS[idx]
    g = full_grid(9, 12, 0)
    g[0][0] = marker
    for r in range(3, 8):
        g[r][5] = 8
    for top, left, cells, color in placements:
        _paint(g, top, left, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_marker":
        # walls and objects without (0,0) marker → no slide direction
        for r in range(3, 8):
            g[r][5] = 8
        _paint(g, 1, 2, [(0, 0), (0, 1), (1, 0)], 5)
        return g
    if name == "no_objects":
        # marker and walls only → nothing to slide
        g[0][0] = 4
        for r in range(3, 8):
            g[r][5] = 8
        return g
    if name == "no_walls":
        # marker and objects without color-8 walls → objects slide off the edge
        g[0][0] = 4
        _paint(g, 1, 2, [(0, 0), (0, 1), (1, 0)], 5)
        _paint(g, 2, 8, [(0, 0), (1, 0), (1, 1)], 6)
        return g
    return g
