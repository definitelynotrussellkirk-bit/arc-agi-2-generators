"""Generator for arc_puzzle_bank_21_set4:S4_H7 — match neutral targets via legend.

Rule: left-side neutral prototypes are paired with nearby color
swatches. Matching neutral shapes on the right side are recolored using
that legend.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, no_swatches, no_right_target.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d2708f8b731b"
VERSION = "1.1.0"
TASK_ID = "d2708f8b731b"
SUMMARY = "A vertical blank separator divides prototype swatches from neutral target shapes."

INVARIANTS = [
    "one empty separator column divides the grid",
    "left-side color-1 prototypes have non-1 swatches to their right",
    "right-side color-1 targets match prototype normalized shapes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "no_swatches", "no_right_target")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "left_legend_with_right_targets",
                       "valid": "left_legend_with_right_targets"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
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
        n_shapes = ctx.draw_int("n_shapes", 2, 2)
    elif difficulty == "hard":
        n_shapes = ctx.draw_int("n_shapes", 3, 3)
    else:
        n_shapes = ctx.draw_int("n_shapes", 2, 3)
    g = full_grid(12, 17, 0)
    sep = 8
    colors = rng.sample([2, 3, 4, 6, 7, 8, 9], n_shapes)
    left_rows = [1, 5, 8]
    right_rows = [1, 5, 8]
    for i in range(n_shapes):
        shape = _SHAPES[i]
        _paint(g, left_rows[i], 1, shape, 1)
        g[left_rows[i] + 1][6] = colors[i]
        _paint(g, right_rows[i], sep + 1, shape, 1)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 17, 0)
    sep = 8
    if name == "no_separator":
        # left + right shapes but no blank separator → cannot split panels
        for i, shape in enumerate(_SHAPES[:2]):
            _paint(g, 1 + 4 * i, 1, shape, 1)
            g[2 + 4 * i][6] = 4
            _paint(g, 1 + 4 * i, sep, shape, 1)   # crosses separator
        return g
    if name == "no_swatches":
        # left prototypes + right targets but no swatch colors → no recolor map
        for i, shape in enumerate(_SHAPES[:2]):
            _paint(g, 1 + 4 * i, 1, shape, 1)
            _paint(g, 1 + 4 * i, sep + 1, shape, 1)
        return g
    if name == "no_right_target":
        # legend complete but no right-side targets → nothing to recolor
        for i, shape in enumerate(_SHAPES[:2]):
            _paint(g, 1 + 4 * i, 1, shape, 1)
            g[2 + 4 * i][6] = 4
        return g
    return g
