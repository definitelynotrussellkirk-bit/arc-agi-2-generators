"""Generator for arc_puzzle_bank_21_set10_s:S10_H6 — complete shape across cross-divided quadrants.

Rule: a full gray row and column divide the grid into four equal
quadrants. One quadrant contains the source shape; the rule fills the
missing symmetric quadrants.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cross, no_shape, multiple_quadrants_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c07088fab0f0"
VERSION = "1.1.0"
TASK_ID = "c07088fab0f0"
SUMMARY = "A single quadrant shape is completed across gray cross-divided quadrants."

INVARIANTS = [
    "one full color-5 row and one full color-5 column divide the grid",
    "exactly one quadrant initially contains a nonzero shape",
    "the source shape has room inside the quadrant under all orientations",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cross", "no_shape", "multiple_quadrants_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "cross_with_one_quad_shape",
                       "valid": "cross_with_one_quad_shape"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    q = 6
    h = w = q * 2 + 1
    g = full_grid(h, w, 0)
    for c in range(w):
        g[q][c] = 5
    for r in range(h):
        g[r][q] = 5
    if difficulty == "easy":
        idx = ctx.draw_int("shape", 0, 1)
    elif difficulty == "hard":
        idx = ctx.draw_int("shape", 2, 3)
    else:
        idx = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
    cells = _SHAPES[idx]
    top = rng.randint(1, q - max(r for r, _c in cells) - 2)
    left = rng.randint(1, q - max(c for _r, c in cells) - 2)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    for r, c in cells:
        g[top + r][left + c] = color
    return g


def _draw_from_degenerate(name, rng):
    q = 6
    h = w = q * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_cross":
        # shape but no gray cross → quadrants undefined
        for r, c in _SHAPES[0]:
            g[1 + r][1 + c] = 4
        return g
    if name == "no_shape":
        # cross drawn but all quadrants empty → nothing to mirror
        for c in range(w): g[q][c] = 5
        for r in range(h): g[r][q] = 5
        return g
    if name == "multiple_quadrants_filled":
        # two quadrants already have shapes → ambiguous source
        for c in range(w): g[q][c] = 5
        for r in range(h): g[r][q] = 5
        for r, c in _SHAPES[0]:
            g[1 + r][1 + c] = 4   # top-left
            g[1 + r][q + 1 + c] = 6   # top-right (different shape/color)
        return g
    return g
