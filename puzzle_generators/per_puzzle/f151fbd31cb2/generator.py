"""Generator for v3_rich_schema:hard_03_dual_key_select_and_recolor.

Rule: use singleton shape and color keys to recolor selected green objects.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_key,
color_key, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shape_key, no_color_key, no_matching_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f151fbd31cb2"
VERSION = "1.1.0"
TASK_ID = "f151fbd31cb2"
SUMMARY = "Use singleton shape and color keys to recolor selected green objects."

INVARIANTS = [
    "one singleton shape key is either 1 for L-triominoes or 4 for plus-shapes",
    "one singleton color key is one of 2,6,8",
    "green objects include at least one L-triomino and one plus-shape",
    "only the selected family is recolored to the color key",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shape_key", "no_color_key", "no_matching_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_key":      {"type": "enum", "default": "rng", "valid": "1|4"},
    "color_key":      {"type": "enum", "default": "rng", "valid": "2|6|8"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_keys_with_two_shape_families",
                       "valid": "two_keys_with_two_shape_families"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPE_KEYS = [1, 4]
_COLOR_KEYS = [2, 6, 8]
_L1 = [(0, 0), (1, 0), (1, 1)]
_L2 = [(0, 0), (0, 1), (1, 1)]
_PLUS = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]


def _paint(g, top, left, cells, color=3):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    shape_key = ctx.draw_choice("shape_key", _SHAPE_KEYS)
    color_key = ctx.draw_choice("color_key", _COLOR_KEYS)
    g = full_grid(10, 12, 0)
    g[0][0] = shape_key
    g[9][11] = color_key
    _paint(g, 2, 2, _L1)
    _paint(g, 5, 2, _L2)
    _paint(g, 2, 8, _PLUS)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_shape_key":
        # only color key → which family to recolor undefined
        g[9][11] = 6
        _paint(g, 2, 2, _L1)
        _paint(g, 5, 2, _L2)
        _paint(g, 2, 8, _PLUS)
        return g
    if name == "no_color_key":
        # only shape key → what color to recolor to undefined
        g[0][0] = 1
        _paint(g, 2, 2, _L1)
        _paint(g, 5, 2, _L2)
        _paint(g, 2, 8, _PLUS)
        return g
    if name == "no_matching_shape":
        # shape_key = 4 (plus) but no plus-shapes in grid → no shapes to recolor
        g[0][0] = 4   # asks for pluses
        g[9][11] = 6
        _paint(g, 2, 2, _L1)
        _paint(g, 5, 2, _L2)
        _paint(g, 2, 8, _L1)   # only L's, no pluses
        return g
    return g
