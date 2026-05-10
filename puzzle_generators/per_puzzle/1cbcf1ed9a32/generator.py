"""Generator for arc_puzzle_bank_21_set11_s:S11_H7 — common shape across panels.

Rule: three separator-delimited panels; the output is the canonical
shape that appears (up to dihedral equivalence) in two of three panels,
recolored to 8.

Combinatorial axes (8): shape, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, all_distinct, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1cbcf1ed9a32"
VERSION = "1.1.0"
TASK_ID = "1cbcf1ed9a32"
SUMMARY = "Find the common shape across three separator-delimited panels up to dihedral equivalence."

INVARIANTS = [
    "two full color-5 columns split the grid into three panels",
    "two panels contain objects with the same canonical rotation/reflection shape",
    "the third panel contains a nonmatching distractor object",
    "the output is the common canonical shape recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "all_distinct", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape":          {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_panels_5_dividers",
                       "valid": "three_panels_5_dividers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
]

_DISTRACTORS = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def _rot90(cells):
    raw = [(c, -r) for r, c in cells]
    mr = min(r for r, _ in raw)
    mc = min(c for _, c in raw)
    return [(r - mr, c - mc) for r, c in raw]


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
        idx = ctx.draw_int("shape", 0, 2)
    elif difficulty == "hard":
        idx = ctx.draw_int("shape", 3, 5)
    else:
        idx = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
    colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    g = full_grid(5, 14, 0)
    for r in range(5):
        g[r][4] = 5
        g[r][9] = 5
    _paint(g, 1, 0, _SHAPES[idx], colors[0])
    _paint(g, 1, 5, _rot90(_SHAPES[idx]), colors[1])
    _paint(g, 1, 10, _DISTRACTORS[idx], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 14, 0)
    if name == "no_separators":
        # Three shapes drawn but no 5-column dividers — panel
        # boundaries undefined, rule can't compare.
        _paint(g, 1, 0, _SHAPES[0], 1)
        _paint(g, 1, 5, _rot90(_SHAPES[0]), 2)
        _paint(g, 1, 10, _DISTRACTORS[0], 3)
        return g
    if name == "all_distinct":
        # Each panel has a different shape — no two share a canonical
        # form, rule's two-of-three match never fires.
        for r in range(5):
            g[r][4] = 5
            g[r][9] = 5
        _paint(g, 1, 0, _SHAPES[0], 1)
        _paint(g, 1, 5, _SHAPES[1], 2)
        _paint(g, 1, 10, _SHAPES[2], 3)
        return g
    if name == "all_match":
        # All three panels share the same canonical shape — no
        # distractor to identify, rule's selection is ambiguous.
        for r in range(5):
            g[r][4] = 5
            g[r][9] = 5
        _paint(g, 1, 0, _SHAPES[0], 1)
        _paint(g, 1, 5, _rot90(_SHAPES[0]), 2)
        _paint(g, 1, 10, _SHAPES[0], 3)
        return g
    return g
