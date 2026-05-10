"""Generator for arc_puzzle_bank_nineteenth21:H133.

The top row is a palette. The body contains separated same-color components
whose areas determine palette rank before the pieces are packed left-to-right.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_components, equal_areas.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "31e43af4bcfa"
VERSION = "1.1.0"
TASK_ID = "31e43af4bcfa"
SUMMARY = "Sort body components by area, recolor by top-row palette, and pack."

INVARIANTS = [
    "the top row has one nonzero palette color per body component",
    "body components are 4-connected color-1 objects separated by background",
    "component areas are distinct, so the palette rank is unambiguous",
    "the canonical rule packs cropped recolored pieces with one blank column gap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_components", "equal_areas")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5..5"},
    "grid_w":         {"type": "int", "default": "8", "valid": "8..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "top_palette_body_components",
                       "valid": "top_palette_body_components"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LAYOUTS = [
    [
        ((1, 1), [(0, 0)]),
        ((4, 1), [(0, 0), (0, 1)]),
        ((1, 5), [(0, 0), (0, 1), (1, 0)]),
    ],
    [
        ((1, 1), [(0, 0)]),
        ((2, 5), [(0, 0), (1, 0)]),
        ((3, 1), [(0, 0), (0, 1), (0, 2), (1, 2)]),
    ],
    [
        ((4, 2), [(0, 0)]),
        ((1, 1), [(0, 0), (1, 0)]),
        ((1, 5), [(0, 0), (0, 1), (1, 1), (2, 1)]),
    ],
]


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
        variant = ctx.draw_int("variant", 0, 0)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 0, 2)
    else:
        variant = ctx.draw_int("variant", 0, 2)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(5, 8, 0)
    for c, color in enumerate(palette):
        g[0][c] = color
    for (top, left), cells in _LAYOUTS[variant]:
        for dr, dc in cells:
            g[top + dr][left + dc] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 8, 0)
    if name == "no_palette":
        # body components but top row is empty → no palette colors to assign
        for (top, left), cells in _LAYOUTS[0]:
            for dr, dc in cells:
                g[top + dr][left + dc] = 1
        return g
    if name == "no_components":
        # palette only, no body components → nothing to rank/recolor
        for c, color in enumerate([2, 3, 4]):
            g[0][c] = color
        return g
    if name == "equal_areas":
        # all components same size → no rank distinction, ambiguous palette assignment
        for c, color in enumerate([2, 3, 4]):
            g[0][c] = color
        # 3 single-cell blobs (all area 1)
        g[2][1] = 1
        g[2][4] = 1
        g[3][6] = 1
        return g
    return g
