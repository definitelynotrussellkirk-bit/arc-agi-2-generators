"""Generator for arc_puzzle_bank_twentysecond21:H152.

Infer a binary support operation from three panels and reuse it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, operation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, no_demo, no_targets.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e4be524bd4b9"
VERSION = "1.1.0"
TASK_ID = "e4be524bd4b9"
SUMMARY = "Infer a binary support operation from three panels and reuse it."

INVARIANTS = [
    "the input has five 3x3 panels split by full color-8 columns",
    "the third panel is the operation result of the first two panels",
    "the target-left panel supplies the output color",
    "the target output is the inferred support operation on panels 4 and 5",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "no_demo", "no_targets")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3..3"},
    "grid_w":         {"type": "int", "default": "19", "valid": "19..19"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "operation":      {"type": "enum", "default": "rng",
                       "valid": "union|intersection|xor"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "5_panels_8col_separated",
                       "valid": "5_panels_8col_separated"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OPS = ["union", "intersection", "xor"]
_EA = {(0, 0), (0, 1), (1, 1)}
_EB = {(0, 1), (1, 0), (1, 1), (2, 2)}
_TA = {(0, 0), (1, 0), (1, 2)}
_TB = {(0, 2), (1, 0), (2, 2)}


def _apply_op(a, b, op):
    if op == "union":
        return a | b
    if op == "intersection":
        return a & b
    return (a | b) - (a & b)


def _paint_panel(g, panel, cells, color):
    left = panel * 4
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
    ex_color = rng.choice([1, 3, 4, 6])
    target_color = rng.choice([2, 5, 7, 9])

    g = full_grid(3, 19, 0)
    for sep in (3, 7, 11, 15):
        for r in range(3):
            g[r][sep] = 8
    panels = [_EA, _EB, _apply_op(_EA, _EB, op), _TA, _TB]
    colors = [ex_color, ex_color, ex_color, target_color, target_color]
    for idx, (cells, color) in enumerate(zip(panels, colors)):
        _paint_panel(g, idx, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 19, 0)
    if name == "no_dividers":
        # missing 8-cols → can't separate panels
        for cells in [_EA, _EB]:
            for r, c in cells: g[r][c] = 4
        return g
    if name == "no_demo":
        # only target operands, no demonstration → operation undefined
        for sep in (3, 7, 11, 15):
            for r in range(3):
                g[r][sep] = 8
        for r, c in _TA: g[r][12 + c] = 5
        for r, c in _TB: g[r][16 + c] = 5
        return g
    if name == "no_targets":
        # demo but no target panels → no operands to apply operation to
        for sep in (3, 7, 11, 15):
            for r in range(3):
                g[r][sep] = 8
        for r, c in _EA: g[r][c] = 4
        for r, c in _EB: g[r][4 + c] = 4
        for r, c in _apply_op(_EA, _EB, "union"): g[r][8 + c] = 4
        return g
    return g
