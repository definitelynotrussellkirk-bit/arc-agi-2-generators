"""Generator for arc_puzzle_bank_twelfth_21_bundle:hard_78_library_decode_select_transform_recolor_shape.

Combinatorial axes (8): grid_h, grid_w, palette_kind, index, transform,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_selector, no_transform_code, no_target_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad8f72a318b2"
VERSION = "1.1.0"
TASK_ID = "ad8f72a318b2"
SUMMARY = "Decode panel index, transform code, and target color from the control strip."

INVARIANTS = [
    "the first four cells of row 0 contain a unary blue panel selector",
    "row 0 column 5 gives the transform code",
    "row 0 column 7 gives the output color",
    "four 4x4 library panels are arranged in a 2x2 grid starting at row 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_selector", "no_transform_code", "no_target_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "index":          {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "transform":      {"type": "int", "default": "rng 1..5", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "control_strip_plus_2x2_panels",
                       "valid": "control_strip_plus_2x2_panels"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]
_POSITIONS = [(2, 0), (2, 5), (7, 0), (7, 5)]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        index = ctx.draw_int("index", 1, 2)
        transform = ctx.draw_int("transform", 1, 2)
    elif difficulty == "hard":
        index = ctx.draw_int("index", 1, 4)
        transform = ctx.draw_int("transform", 3, 5)
    else:
        index = ctx.draw_int("index", 1, 4)
        transform = ctx.draw_int("transform", 1, 5)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8], 4)
    target = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c not in colors])
    g = full_grid(11, 9, 0)
    for c in range(index):
        g[0][c] = 1
    g[0][5] = transform
    g[0][7] = target
    for (top, left), cells, color in zip(_POSITIONS, _SHAPES, colors):
        _paint(g, top, left, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 9, 0)
    # always paint the panels so degenerate isn't entirely empty
    colors = [2, 3, 4, 5]
    for (top, left), cells, color in zip(_POSITIONS, _SHAPES, colors):
        _paint(g, top, left, cells, color)
    if name == "no_selector":
        # control strip missing the unary index → no panel can be selected
        g[0][5] = 2
        g[0][7] = 9
        return g
    if name == "no_transform_code":
        # selector + target but missing transform code → no operation defined
        g[0][0] = 1; g[0][1] = 1
        g[0][7] = 9
        return g
    if name == "no_target_color":
        # selector + transform but no output color → result has no color to use
        g[0][0] = 1; g[0][1] = 1
        g[0][5] = 2
        return g
    return g
