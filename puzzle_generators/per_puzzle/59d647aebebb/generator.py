"""Generator for arc_puzzle_bank_twentythird21:H157.

Infer a binary set operation, including left-minus, from five panels.

Combinatorial axes (8): grid_h, grid_w, palette_kind, operation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, no_demo, identical_operands.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "59d647aebebb"
VERSION = "1.1.0"
TASK_ID = "59d647aebebb"
SUMMARY = "Infer a binary set operation, including left-minus, from five panels."

INVARIANTS = [
    "the input has five 4x4 panels separated by full color-8 columns",
    "the first three panels demonstrate union, intersection, xor, or left-minus",
    "the fourth and fifth panels are the target operands",
    "the output is the same operation applied to the target pair",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "no_demo", "identical_operands")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "24", "valid": "24..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "operation":      {"type": "enum", "default": "rng",
                       "valid": "union|intersection|xor|left-minus"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "5_panels_8col_separated",
                       "valid": "5_panels_8col_separated"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OPS = ["union", "intersection", "xor", "left-minus"]
_EA = {(0, 0), (0, 1), (1, 1), (2, 0)}
_EB = {(0, 1), (1, 0), (1, 1), (2, 2)}
_X = {(0, 0), (0, 2), (1, 1), (2, 2)}
_Y = {(0, 2), (1, 0), (1, 1), (3, 3)}


def _apply_op(a, b, op):
    if op == "union":
        return a | b
    if op == "intersection":
        return a & b
    if op == "xor":
        return (a | b) - (a & b)
    return a - b


def _paint_panel(g, panel, cells, color):
    left = panel * 5
    for r, c in cells:
        g[r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        op = ctx.draw_choice("operation", ["union", "intersection"])
    elif difficulty == "hard":
        op = ctx.draw_choice("operation", _OPS)
    else:
        op = ctx.draw_choice("operation", _OPS)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])

    g = full_grid(4, 24, 0)
    for sep in (4, 9, 14, 19):
        for r in range(4):
            g[r][sep] = 8
    panels = [_EA, _EB, _apply_op(_EA, _EB, op), _X, _Y]
    for idx, cells in enumerate(panels):
        _paint_panel(g, idx, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 24, 0)
    if name == "no_dividers":
        # missing 8-cols → can't separate 5 panels
        for cells in [_EA, _EB]:
            for r, c in cells: g[r][c] = 4
        return g
    if name == "no_demo":
        # only target panels, no demo of A op B = C → operation undefined
        for sep in (4, 9, 14, 19):
            for r in range(4):
                g[r][sep] = 8
        for r, c in _X: g[r][15 + c] = 4
        for r, c in _Y: g[r][20 + c] = 4
        return g
    if name == "identical_operands":
        # demo with A == B → all 4 ops collapse, can't disambiguate
        for sep in (4, 9, 14, 19):
            for r in range(4):
                g[r][sep] = 8
        cells = {(0, 0), (1, 1), (2, 2)}
        for r, c in cells: g[r][c] = 4; g[r][5 + c] = 4; g[r][10 + c] = 4
        for r, c in _X: g[r][15 + c] = 4
        for r, c in _Y: g[r][20 + c] = 4
        return g
    return g
