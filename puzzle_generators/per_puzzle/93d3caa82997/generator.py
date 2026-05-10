"""Generator for arc_puzzle_bank_seventh_21_bundle:hard_45_overlay_selected_components_with_rotation.

The first row selects two component colors. The first component is overlaid
with a clockwise rotation of the second; overlaps become color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_selectors, no_objects, identical_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "93d3caa82997"
VERSION = "1.1.0"
TASK_ID = "93d3caa82997"
SUMMARY = "Overlay one selected component with the clockwise rotation of another."

INVARIANTS = [
    "the first row contains two nonzero selector colors",
    "the body contains one object for each selector color",
    "selected objects are separated from each other",
    "the output overlays object A with rotated object B, marking overlap as 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_selectors", "no_objects", "identical_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_variant":  {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_selectors_plus_two_objects",
                       "valid": "row0_selectors_plus_two_objects"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_A_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
]
_B_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        variant = ctx.draw_int("shape_variant", 0, 0)
    elif difficulty == "hard":
        variant = ctx.draw_int("shape_variant", 1, 1)
    else:
        variant = ctx.draw_int("shape_variant", 0, 1)
    a, b = rng.sample([2, 3, 4, 5, 6, 7], 2)
    g = full_grid(9, 11, 0)
    g[0][1] = a
    g[0][3] = b
    _paint(g, 2, 1, _A_SHAPES[variant], a)
    _paint(g, 2, 7, _B_SHAPES[variant], b)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 11, 0)
    if name == "no_selectors":
        # objects without row-0 selectors → no choice for which two to overlay
        _paint(g, 2, 1, _A_SHAPES[0], 4)
        _paint(g, 2, 7, _B_SHAPES[0], 6)
        return g
    if name == "no_objects":
        # selectors alone, no body objects → nothing to overlay
        g[0][1] = 4
        g[0][3] = 6
        return g
    if name == "identical_shapes":
        # both selected objects share shape → rotated overlay equals A (no signal)
        g[0][1] = 4; g[0][3] = 6
        _paint(g, 2, 1, _A_SHAPES[0], 4)
        _paint(g, 2, 7, _A_SHAPES[0], 6)
        return g
    return g
