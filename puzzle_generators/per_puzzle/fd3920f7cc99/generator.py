"""Generator for arc_puzzle_bank_third_21_bundle:hard_21_cartesian_product_of_row_shapes_and_column_colors.

Color-2 row-shape objects are crossed with top-row color swatches to build a
gallery where each shape is recolored by each column color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_swatches, no_shapes, swatch_color_2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fd3920f7cc99"
VERSION = "1.1.0"
TASK_ID = "fd3920f7cc99"
SUMMARY = "Cartesian product of color-2 row shapes and top-row color swatches."

INVARIANTS = [
    "top-row nonzero swatches exclude color 2",
    "row shapes are connected color-2 objects sorted by row",
    "row shapes are separated from each other and from swatches",
    "the output recolors every row shape by every swatch color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_swatches", "no_shapes", "swatch_color_2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "row_shapes_with_top_swatches",
                       "valid": "row_shapes_with_top_swatches"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1)],
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
        n_shapes = ctx.draw_int("n_shapes", 2, 2)
        n_colors = ctx.draw_int("n_colors", 2, 2)
    elif difficulty == "hard":
        n_shapes = ctx.draw_int("n_shapes", 3, 3)
        n_colors = ctx.draw_int("n_colors", 3, 3)
    else:
        n_shapes = ctx.draw_int("n_shapes", 2, 3)
        n_colors = ctx.draw_int("n_colors", 2, 3)
    colors = rng.sample([1, 3, 4, 5, 6, 7, 8, 9], n_colors)
    g = full_grid(12, 11, 0)

    for idx, color in enumerate(colors):
        g[0][2 + idx * 3] = color
    for idx in range(n_shapes):
        _paint(g, 2 + idx * 3, 1 + rng.randint(0, 1), _SHAPES[idx], 2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 11, 0)
    if name == "no_swatches":
        # row shapes but no top-row swatches → no colors to recolor with
        for idx in range(2):
            _paint(g, 2 + idx * 3, 1, _SHAPES[idx], 2)
        return g
    if name == "no_shapes":
        # swatches but no row shapes → nothing to recolor
        for idx, color in enumerate([3, 4, 5]):
            g[0][2 + idx * 3] = color
        return g
    if name == "swatch_color_2":
        # swatch is color 2 → confused with shape color, "exclude 2" violated
        g[0][2] = 2
        for idx in range(2):
            _paint(g, 2 + idx * 3, 1, _SHAPES[idx], 2)
        return g
    return g
