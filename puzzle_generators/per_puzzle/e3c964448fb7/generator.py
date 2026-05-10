"""Generator for arc_puzzle_bank_tenth21:M69.

Rule: above a separator row, each color defines a prototype shape.
Below it, a key color selects one prototype and an 8 marks where to stamp it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, selected_index,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, no_anchor, key_not_in_library.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e3c964448fb7"
VERSION = "1.1.0"
TASK_ID = "e3c964448fb7"
SUMMARY = "A lower key color selects an upper prototype and stamps it at an 8 anchor."

INVARIANTS = [
    "one full color-9 row separates prototype library and query",
    "prototype colors are unique",
    "the lower section has exactly one non-8 key color and one color-8 anchor",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "no_anchor", "key_not_in_library")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "selected_index": {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "library_separator_query",
                       "valid": "library_separator_query"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "4..6"},
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
        selected = ctx.draw_int("selected_index", 0, 0)
    elif difficulty == "hard":
        selected = ctx.draw_int("selected_index", 1, 2)
    else:
        selected = ctx.draw_int("selected_index", 0, 2)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7], 3)
    g = full_grid(12, 14, 0)
    for i, (shape, color) in enumerate(zip(_SHAPES, colors)):
        _paint(g, 1, 1 + i * 4, shape, color)
    for c in range(14):
        g[5][c] = 9
    g[8][2] = colors[selected]
    g[8][7] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    colors = [4, 6, 3]
    for i, (shape, color) in enumerate(zip(_SHAPES, colors)):
        _paint(g, 1, 1 + i * 4, shape, color)
    if name == "no_separator":
        # no 9-row → library/query split undefined
        g[8][2] = 4; g[8][7] = 8
        return g
    for c in range(14): g[5][c] = 9
    if name == "no_anchor":
        # key but no 8 anchor → no destination position
        g[8][2] = 4   # only the key, no 8
        return g
    if name == "key_not_in_library":
        # key color not in prototype library → lookup fails
        g[8][2] = 7   # 7 not in colors=[4, 6, 3]
        g[8][7] = 8
        return g
    return g
