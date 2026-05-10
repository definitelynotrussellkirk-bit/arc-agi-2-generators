"""Generator for arc_puzzle_bank_third21:H20.

Rule: show three translated copies and leave the fourth rectangle
corner blank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape, palette_size,
position_bias, n_distinct_colors, missing_corner, texture.
Degenerates: only_two_copies, four_copies, mismatched_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "441c97bcdb07"
VERSION = "1.1.0"
TASK_ID = "441c97bcdb07"
SUMMARY = "Show three translated copies and leave the fourth rectangle corner blank."

INVARIANTS = [
    "there are exactly three same-color copies of one 4-connected shape",
    "two copies share the pivot row and two share the pivot column",
    "the missing copy location is inside the grid and initially blank",
    "the canonical rule paints the fourth translated copy",
]

PALETTE_KINDS = ("default", "L_shape", "Z_shape", "T_shape")
DEGENERATE_TEXTURES = ("only_two_copies", "four_copies", "mismatched_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "three_corners",
                       "valid": "three_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "missing_corner": {"type": "str", "default": "br", "valid": "br"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("shape", 0, 0)
    elif difficulty == "hard":
        idx = ctx.draw_int("shape", 1, 2)
    else:
        idx = ctx.draw_int("shape", 0, 2)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    cells = _SHAPES[idx]

    g = full_grid(10, 10, 0)
    for top, left in [(1, 1), (1, 6), (6, 1)]:
        _paint(g, top, left, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    cells = _SHAPES[0]
    if name == "only_two_copies":
        # only two copies → fourth corner can't be inferred uniquely
        for top, left in [(1, 1), (1, 6)]:
            _paint(g, top, left, cells, 4)
        return g
    if name == "four_copies":
        # all four corners filled → rule has no missing corner to add
        for top, left in [(1, 1), (1, 6), (6, 1), (6, 6)]:
            _paint(g, top, left, cells, 4)
        return g
    if name == "mismatched_shapes":
        # three copies but with different shapes → no consistent template
        _paint(g, 1, 1, _SHAPES[0], 4)
        _paint(g, 1, 6, _SHAPES[1], 4)
        _paint(g, 6, 1, _SHAPES[2], 4)
        return g
    return g
