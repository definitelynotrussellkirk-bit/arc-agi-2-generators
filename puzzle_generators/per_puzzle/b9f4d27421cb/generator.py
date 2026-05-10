"""Generator for arc_puzzle_bank_twelfth21:H82.

Rule: top pair shows geometric transform, mid pair shows recolor map,
apply both to query at bottom-left.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_query, no_recolor_map.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9f4d27421cb"
VERSION = "1.1.0"
TASK_ID = "b9f4d27421cb"
SUMMARY = "Learn geometry from one example pair and recoloring from another, then fill the query panel."

INVARIANTS = [
    "two full color-9 rows and one full color-9 column split a 3x2 example/query layout",
    "the top pair demonstrates one geometric transform",
    "the middle pair demonstrates a nonzero color substitution map",
    "the bottom-left query is transformed and recolored into the blank bottom-right panel",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_query", "no_recolor_map")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "int", "default": "rng 1..5", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "3x2_example_query",
                       "valid": "3x2_example_query"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TOP = [
    [2, 0, 0, 0],
    [2, 2, 0, 0],
    [0, 2, 0, 0],
    [0, 2, 2, 0],
]
_MID_LEFT = [
    [2, 0, 3, 0],
    [0, 4, 0, 0],
    [3, 0, 2, 0],
    [0, 0, 0, 4],
]
_MID_RIGHT = [
    [6, 0, 7, 0],
    [0, 8, 0, 0],
    [7, 0, 6, 0],
    [0, 0, 0, 8],
]
_QUERY = [
    [2, 0, 0, 0],
    [3, 2, 0, 0],
    [0, 4, 4, 0],
    [0, 0, 3, 0],
]


def _rot90(g):
    return [[g[len(g) - 1 - r][c] for r in range(len(g))] for c in range(len(g[0]))]


def _rot180(g):
    return _rot90(_rot90(g))


def _rot270(g):
    return _rot90(_rot180(g))


def _hflip(g):
    return [list(reversed(row)) for row in g]


def _transform(g, code):
    return {1: g, 2: _rot90(g), 3: _rot180(g), 4: _rot270(g), 5: _hflip(g)}[code]


def _paste(g, top, left, sub):
    for r, row in enumerate(sub):
        for c, v in enumerate(row):
            g[top + r][left + c] = v


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    code = ctx.draw_int("transform", 1, 5)
    g = full_grid(14, 9, 0)
    for r in (4, 9):
        for c in range(9):
            g[r][c] = 9
    for r in range(14):
        g[r][4] = 9
    _paste(g, 0, 0, _TOP)
    _paste(g, 0, 5, _transform(_TOP, code))
    _paste(g, 5, 0, _MID_LEFT)
    _paste(g, 5, 5, _MID_RIGHT)
    _paste(g, 10, 0, _QUERY)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 9, 0)
    if name == "no_separators":
        # No 9-dividers — rule's 6-panel split fails; example/query
        # boundaries undefined.
        _paste(g, 0, 0, _TOP)
        _paste(g, 5, 0, _MID_LEFT)
        _paste(g, 10, 0, _QUERY)
        return g
    for r in (4, 9):
        for c in range(9): g[r][c] = 9
    for r in range(14): g[r][4] = 9
    if name == "no_query":
        # Examples shown but bottom-left empty — rule has nothing
        # to apply transform+recolor to.
        _paste(g, 0, 0, _TOP)
        _paste(g, 0, 5, _hflip(_TOP))
        _paste(g, 5, 0, _MID_LEFT)
        _paste(g, 5, 5, _MID_RIGHT)
        return g
    if name == "no_recolor_map":
        # Mid example identical L=R — rule's recolor map is identity;
        # rule's recolor branch has no visible effect.
        _paste(g, 0, 0, _TOP)
        _paste(g, 0, 5, _hflip(_TOP))
        _paste(g, 5, 0, _MID_LEFT)
        _paste(g, 5, 5, _MID_LEFT)
        _paste(g, 10, 0, _QUERY)
        return g
    return g
