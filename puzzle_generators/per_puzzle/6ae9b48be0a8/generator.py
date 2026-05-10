"""Generator for arc_puzzle_bank_21_set2:S2_H7.

Three green objects appear; two share the same normalized shape and one is the
odd shape out. The rule draws a yellow border around the unique shape.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_family,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_same_shape, all_distinct_shapes, single_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6ae9b48be0a8"
VERSION = "1.1.0"
TASK_ID = "6ae9b48be0a8"
SUMMARY = "Two repeated green shapes and one unique green shape, with room for an outside border."

INVARIANTS = [
    "all foreground objects are color 3",
    "exactly two objects share one normalized shape",
    "the unique object has a one-cell margin for the output border",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_shape", "all_distinct_shapes", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_family":   {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "two_pair_one_unique",
                       "valid": "two_pair_one_unique"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PAIRS = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]
_UNIQUES = [
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
]


def _paint(g, top, left, cells):
    for r, c in cells:
        g[top + r][left + c] = 3


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        family = ctx.draw_int("shape_family", 0, 0)
    elif difficulty == "hard":
        family = ctx.draw_int("shape_family", 0, len(_PAIRS) - 1)
    else:
        family = ctx.draw_int("shape_family", 0, len(_PAIRS) - 1)
    unique_index = ctx.draw_int("unique_index", 0, 2)
    g = full_grid(13, 15, 0)
    slots = [(2, 2), (2, 9), (8, 5)]
    rng.shuffle(slots)
    for i, slot in enumerate(slots):
        cells = _UNIQUES[family] if i == unique_index else _PAIRS[family]
        _paint(g, slot[0], slot[1], cells)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 15, 0)
    if name == "all_same_shape":
        # 3 identical shapes → no unique shape to border
        for slot in [(2, 2), (2, 9), (8, 5)]:
            _paint(g, slot[0], slot[1], _PAIRS[0])
        return g
    if name == "all_distinct_shapes":
        # 3 distinct shapes → no pair of repeated shapes, "odd one out" undefined
        _paint(g, 2, 2, _PAIRS[0])
        _paint(g, 2, 9, _PAIRS[1])
        _paint(g, 8, 5, _UNIQUES[0])
        return g
    if name == "single_shape":
        # only 1 shape → no comparison possible
        _paint(g, 5, 5, _PAIRS[0])
        return g
    return g
