"""Generator for arc_puzzle_bank_thirteenth21:H91 — infer binary op then apply.

Rule: top row has 3 panels (a, b, op(a,b)); bottom row starts with
(d, e, ?). Infer op from top, apply to bottom pair, paint result in 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identical_pair (a==b → union==intersection==a, xor=∅,
all 3 ops indistinguishable), empty_operands (a or b empty → ops
collapse: union=other, intersection=∅, xor=other), bottom_identical
(d==e → output is also non-discriminative).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a20ecf84f041"
VERSION = "1.1.0"
TASK_ID = "a20ecf84f041"
SUMMARY = "Infer union/intersection/xor from the top triplet and apply it below."

INVARIANTS = [
    "the grid has two rows of three 3x3 panels separated by color-9 lines",
    "the top-right panel is the selected binary operation on the top pair",
    "the lower-right panel starts blank",
    "the inferred lower result is painted in color 2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identical_pair", "empty_operands", "bottom_identical")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "operation":      {"type": "enum", "default": "rng", "valid": "union|intersection|xor"},
    "variant":        {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_row_three_panel",
                       "valid": "two_row_three_panel"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OPS = ["union", "intersection", "xor"]
_PATTERNS = [
    (
        {(0, 0), (0, 1), (1, 0), (2, 2)},
        {(0, 1), (1, 1), (2, 0), (2, 2)},
        {(0, 0), (0, 2), (1, 2)},
        {(0, 2), (1, 0), (1, 2)},
    ),
    (
        {(0, 0), (1, 0), (1, 1), (2, 1)},
        {(0, 2), (1, 1), (1, 2), (2, 0)},
        {(0, 1), (1, 1), (2, 1)},
        {(0, 0), (1, 1), (2, 2)},
    ),
    (
        {(0, 1), (0, 2), (1, 1), (2, 0)},
        {(0, 0), (1, 1), (2, 0), (2, 2)},
        {(0, 0), (1, 0), (2, 0), (2, 1)},
        {(0, 2), (1, 1), (2, 1)},
    ),
    (
        {(0, 0), (1, 0), (2, 0), (2, 1)},
        {(0, 1), (1, 1), (1, 2), (2, 1)},
        {(0, 0), (0, 1), (1, 1)},
        {(1, 0), (1, 1), (2, 2)},
    ),
    (
        {(0, 2), (1, 0), (1, 1), (1, 2)},
        {(0, 0), (1, 1), (2, 1), (2, 2)},
        {(0, 1), (0, 2), (1, 2)},
        {(0, 0), (1, 1), (2, 0), (2, 1)},
    ),
]


def _apply(a, b, op):
    if op == "union":
        return a | b
    if op == "intersection":
        return a & b
    return (a | b) - (a & b)


def _paint_panel(g, row_band, panel, cells, color=2):
    top = row_band * 4
    left = panel * 4
    for r, c in cells:
        g[top + r][left + c] = color


def _make_separators(g):
    for c in (3, 7):
        for r in range(7):
            g[r][c] = 9
    for c in range(11):
        g[3][c] = 9


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    op = ctx.draw_choice("operation", _OPS)
    variant = ctx.draw_int("variant", 0, 4)
    a, b, d, e = _PATTERNS[variant]
    g = full_grid(7, 11, 0)
    _make_separators(g)
    for idx, cells in enumerate([a, b, _apply(a, b, op)]):
        _paint_panel(g, 0, idx, cells)
    _paint_panel(g, 1, 0, d)
    _paint_panel(g, 1, 1, e)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 11, 0)
    _make_separators(g)
    if name == "identical_pair":
        # Top a==b → union==intersection==a, xor=∅; rule cannot
        # distinguish ops from the top triplet.
        a = {(0, 0), (1, 1), (2, 2)}
        d = {(0, 0), (0, 1), (1, 1)}
        e = {(1, 0), (1, 1), (2, 2)}
        for idx, cells in enumerate([a, a, a]):
            _paint_panel(g, 0, idx, cells)
        _paint_panel(g, 1, 0, d)
        _paint_panel(g, 1, 1, e)
        return g
    if name == "empty_operands":
        # Top a is empty → union=b, intersection=∅, xor=b; only
        # intersection vs the others is distinguishable.
        a = set()
        b = {(0, 0), (1, 1), (2, 2)}
        d = {(0, 1), (1, 1)}
        e = {(1, 1), (2, 2)}
        for idx, cells in enumerate([a, b, b]):
            _paint_panel(g, 0, idx, cells)
        _paint_panel(g, 1, 0, d)
        _paint_panel(g, 1, 1, e)
        return g
    if name == "bottom_identical":
        # Bottom d==e → applied op also collapses; output is
        # non-discriminative regardless of inferred op.
        a = {(0, 0), (0, 1), (1, 0)}
        b = {(0, 1), (1, 1), (2, 1)}
        d = {(0, 0), (1, 1), (2, 2)}
        for idx, cells in enumerate([a, b, _apply(a, b, "union")]):
            _paint_panel(g, 0, idx, cells)
        _paint_panel(g, 1, 0, d)
        _paint_panel(g, 1, 1, d)
        return g
    return g
