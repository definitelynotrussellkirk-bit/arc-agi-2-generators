"""Generator for arc_additional_puzzle_bank_volume8:E55.

Rule: red components that touch any grid corner are recolored green.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_corner_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_objects, no_interior_objects, all_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "778a00c38b8d"
VERSION = "1.1.0"
TASK_ID = "778a00c38b8d"
SUMMARY = "Red components that touch any grid corner are recolored green."

INVARIANTS = [
    "background is 0",
    "at least one red component touches a corner",
    "interior red components do not touch any corner",
    "red components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_objects", "no_interior_objects", "all_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_corner_components": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "corner_anchored_plus_interior",
                       "valid": "corner_anchored_plus_interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_cells(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_corner_components = ctx.draw_int("n_corner_components", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_corner_components = ctx.draw_int("n_corner_components", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_corner_components = ctx.draw_int("n_corner_components", 1, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    corner_shapes = {
        (0, 0): [(0, 0), (0, 1), (1, 0)],
        (0, w - 1): [(0, w - 1), (0, w - 2), (1, w - 1)],
        (h - 1, 0): [(h - 1, 0), (h - 2, 0), (h - 1, 1)],
        (h - 1, w - 1): [(h - 1, w - 1), (h - 2, w - 1), (h - 1, w - 2)],
    }
    corners = list(corner_shapes)
    rng.shuffle(corners)
    for corner in corners[:n_corner_components]:
        _paint_cells(g, corner_shapes[corner], 2)

    for _ in range(rng.randint(1, 3)):
        r = rng.randint(2, h - 4)
        c = rng.randint(2, w - 4)
        shape = [(r, c), (r, c + 1), (r + 1, c)]
        if all(g[rr][cc] == 0 for rr, cc in shape):
            _paint_cells(g, shape, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_corner_objects":
        # only interior red components → rule fires zero times, output identical
        for (r, c) in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 2
        for (r, c) in [(6, 6), (6, 7), (7, 6)]: g[r][c] = 2
        return g
    if name == "no_interior_objects":
        # only corner-touching components → all recolored
        for (r, c) in [(0, 0), (0, 1), (1, 0)]: g[r][c] = 2
        for (r, c) in [(h - 1, w - 1), (h - 1, w - 2), (h - 2, w - 1)]: g[r][c] = 2
        return g
    if name == "all_corner":
        # red components at all 4 corners with nothing interior → all recolored
        for (r, c) in [(0, 0), (0, 1), (1, 0)]: g[r][c] = 2
        for (r, c) in [(0, w - 1), (0, w - 2), (1, w - 1)]: g[r][c] = 2
        for (r, c) in [(h - 1, 0), (h - 1, 1), (h - 2, 0)]: g[r][c] = 2
        for (r, c) in [(h - 1, w - 1), (h - 1, w - 2), (h - 2, w - 1)]: g[r][c] = 2
        return g
    return g
