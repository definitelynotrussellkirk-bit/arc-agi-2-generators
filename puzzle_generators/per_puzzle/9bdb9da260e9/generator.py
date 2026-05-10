"""Generator for arc_puzzle_bank_21_set3:S3_H1 — colored legend recolors gray copies.

Rule: the top band is a color/shape legend. The lower band contains
gray copies of those shapes that should be recolored by matching the
legend shape.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_targets, missing_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9bdb9da260e9"
VERSION = "1.1.0"
TASK_ID = "9bdb9da260e9"
SUMMARY = "Colored legend shapes above an empty row recolor gray copies below it."

INVARIANTS = [
    "one all-zero row separates legend and target bands",
    "legend shapes have distinct normalized forms and colors",
    "target shapes are gray copies of legend shapes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_targets", "missing_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "two_band_legend_with_targets",
                       "valid": "two_band_legend_with_targets"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
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
    g = full_grid(12, 15, 0)
    colors = rng.sample([2, 3, 4, 6, 7, 8, 9], n_shapes)
    legend_cols = [1, 6, 11]
    target_cols = [2, 7, 11]
    for i in range(n_shapes):
        cells = _SHAPES[i]
        _paint(g, 1, legend_cols[i], cells, colors[i])
        _paint(g, 6 + (i % 2), target_cols[i], cells, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 15, 0)
    if name == "no_legend":
        # gray targets but no legend → no recolor mapping
        _paint(g, 7, 2, _SHAPES[0], 5)
        _paint(g, 7, 7, _SHAPES[1], 5)
        return g
    if name == "no_targets":
        # legend present but no gray targets → rule has nothing to recolor
        _paint(g, 1, 1, _SHAPES[0], 4)
        _paint(g, 1, 6, _SHAPES[1], 6)
        return g
    if name == "missing_match":
        # target shape doesn't match any legend shape → lookup fails
        _paint(g, 1, 1, _SHAPES[0], 4)
        _paint(g, 1, 6, _SHAPES[1], 6)
        # Target is shape 2 (plus), but no legend entry for that
        _paint(g, 7, 2, _SHAPES[2], 5)
        return g
    return g
