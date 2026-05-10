"""Generator for arc_puzzle_bank_tenth21:M65 — palette recolors size-ranked 8-components.

Rule: the top row supplies a palette. Placeholder color-8 components in the body
are sorted by size and recolored in palette order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_components, tied_component_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "627260bf308f"
VERSION = "1.1.0"
TASK_ID = "627260bf308f"
SUMMARY = "Palette colors recolor size-ranked placeholder-8 components."

INVARIANTS = [
    "top row has nonzero palette colors excluding placeholder color 8",
    "body components are color 8 and have distinct sizes",
    "there is one palette entry for each placeholder component",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_components", "tied_component_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "header_palette_with_components",
                       "valid": "header_palette_with_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
]


def _paint(g, top, left, cells):
    for r, c in cells:
        g[top + r][left + c] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_components = ctx.draw_int("n_components", 2, 2)
    elif difficulty == "hard":
        n_components = ctx.draw_int("n_components", 3, 4)
    else:
        n_components = ctx.draw_int("n_components", 2, 4)
    g = full_grid(13, 16, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n_components)
    for i, color in enumerate(palette):
        g[0][1 + i * 2] = color
    origins = [(2, 1), (2, 7), (8, 1), (7, 9)]
    for i in range(n_components):
        _paint(g, origins[i][0], origins[i][1], _SHAPES[i])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 16, 0)
    if name == "no_palette":
        # body components but no row-0 palette → no recolor mapping
        _paint(g, 2, 1, _SHAPES[0])
        _paint(g, 2, 7, _SHAPES[1])
        return g
    if name == "no_components":
        # palette but no 8-components → nothing to recolor
        g[0][1] = 4; g[0][3] = 6; g[0][5] = 7
        return g
    if name == "tied_component_sizes":
        # two components have the same size → ambiguous size rank
        g[0][1] = 4; g[0][3] = 6
        _paint(g, 2, 1, _SHAPES[0])    # size 3
        _paint(g, 7, 7, _SHAPES[0])    # size 3 (tied)
        return g
    return g
