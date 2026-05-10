"""Generator for arc_puzzle_bank_next21:H9 — XOR of normalized supports.

Rule: color-2 and color-3 objects are normalized to their own bounding
boxes. The rule outputs color 8 where exactly one normalized shape
has a cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_pair,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: identical_shapes, no_overlap, missing_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3cdfed241796"
VERSION = "1.1.0"
TASK_ID = "3cdfed241796"
SUMMARY = "Two colored shapes produce the XOR of their normalized supports."

INVARIANTS = [
    "there is exactly one color-2 object and one color-3 object",
    "the objects are spatially separated",
    "their normalized supports differ",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identical_shapes", "no_overlap", "missing_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_pair":     {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_separated_color_shapes",
                       "valid": "two_separated_color_shapes"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PAIRS = [
    ([(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, 1), (1, 1), (2, 1)]),
    ([(0, 1), (1, 0), (1, 1), (1, 2)], [(0, 0), (1, 0), (1, 1), (2, 0)]),
    ([(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)], [(0, 0), (1, 0), (2, 0), (2, 1)]),
    ([(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 1), (1, 1), (2, 0), (2, 1)]),
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
    if difficulty == "easy":
        pair = ctx.draw_int("shape_pair", 0, 0)
    elif difficulty == "hard":
        pair = ctx.draw_int("shape_pair", 2, 3)
    else:
        pair = ctx.draw_int("shape_pair", 0, len(_PAIRS) - 1)
    rng = ctx.draw_rng("layout")
    g = full_grid(10, 14, 0)
    a, b = _PAIRS[pair]
    _paint(g, rng.randint(1, 3), 1, a, 2)
    _paint(g, rng.randint(4, 6), 9, b, 3)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 14, 0)
    same = [(0, 0), (1, 0), (1, 1), (2, 1)]
    if name == "identical_shapes":
        # 2-shape and 3-shape are identical (normalized) → XOR is empty (output blank)
        _paint(g, 2, 1, same, 2)
        _paint(g, 5, 9, same, 3)
        return g
    if name == "no_overlap":
        # normalized supports are disjoint → XOR equals union (rule observable)
        # but this is actually a *helpful* case; mark it as the precondition-violation:
        # support-difference invariant says "differ" — disjoint also differs but trivially
        a = [(0, 0), (1, 1)]   # diagonal
        b = [(0, 1), (1, 0)]   # anti-diagonal — disjoint after normalize
        _paint(g, 2, 1, a, 2)
        _paint(g, 5, 9, b, 3)
        return g
    if name == "missing_color":
        # only color-2 present, no color-3 → "exactly one color-3 object" precondition fails
        _paint(g, 2, 1, same, 2)
        return g
    return g
