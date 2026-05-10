"""Generator for arc_puzzle_bank_fifth21:H31 — rotate BL quadrant into BR quadrant.

Rule: a shape in the bottom-left quadrant is rotated 90 degrees into
the bottom-right quadrant. A color-9 row and column define the
quadrant split.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_split, no_shape, br_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9d2f7c9e2ac4"
VERSION = "1.1.0"
TASK_ID = "9d2f7c9e2ac4"
SUMMARY = "Rotate the bottom-left quadrant shape into the bottom-right quadrant."

INVARIANTS = [
    "a full color-9 row and full color-9 column split the grid into quadrants",
    "the bottom-left quadrant contains one nonzero same-color shape",
    "the bottom-right quadrant is initially empty",
    "the shape fits after rotation into the bottom-right quadrant",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_split", "no_shape", "br_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "split_with_bl_shape",
                       "valid": "split_with_bl_shape"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape = _SHAPES[ctx.draw_int("shape_variant", 0, 0)]
    elif difficulty == "hard":
        shape = _SHAPES[ctx.draw_int("shape_variant", 1, 2)]
    else:
        shape = _SHAPES[ctx.draw_int("shape_variant", 0, len(_SHAPES) - 1)]
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    g = full_grid(9, 9, 0)
    for i in range(9):
        g[4][i] = 9
        g[i][4] = 9
    _paint(g, 5 + rng.randint(0, 1), rng.randint(0, 1), shape, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_split":
        # shape but no 9-row/col → no quadrant split defined
        _paint(g, 5, 1, _SHAPES[0], 4)
        return g
    if name == "no_shape":
        # split present but BL quadrant is empty → nothing to rotate
        for i in range(9):
            g[4][i] = 9; g[i][4] = 9
        return g
    if name == "br_already_filled":
        # BR quadrant already has cells → rotation target collides
        for i in range(9):
            g[4][i] = 9; g[i][4] = 9
        _paint(g, 5, 1, _SHAPES[0], 4)
        _paint(g, 6, 6, _SHAPES[2], 6)
        return g
    return g
