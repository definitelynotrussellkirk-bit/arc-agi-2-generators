"""Generator for arc_puzzle_bank_fourteenth21:H96.

Rule: 9x9 grid is split by color-9 row and column into 4x4 panels.
Top-right = top-left + relative additions; the same additions are
painted at bottom-left in the query color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, no_q_panel, identical_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a80c6418f6bc"
VERSION = "1.1.0"
TASK_ID = "a80c6418f6bc"
SUMMARY = "Transfer relative addition cells from the top example to the query."

INVARIANTS = [
    "the 9x9 grid is split by color-9 row and column into 4x4 panels",
    "top-right equals top-left plus relative addition cells",
    "bottom-left is copied into the blank bottom-right panel",
    "the same additions are painted in the query color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "no_q_panel", "identical_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

_A = {(0, 0), (0, 1), (1, 0)}
_ADDS = [
    {(1, 1), (2, 1)},
    {(0, 2), (1, 1)},
    {(1, 1), (2, 0), (2, 1)},
]
_Q = {(0, 0), (0, 1), (1, 0)}

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_4_panel",
                       "valid": "fixed_4_panel"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "panels", "valid": "panels"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
        variant = ctx.draw_int("variant", 0, 0)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 1, 2)
    else:
        variant = ctx.draw_int("variant", 0, 2)
    a_color = rng.choice([1, 2, 4, 5])
    q_color = rng.choice([3, 5, 6, 7])

    g = full_grid(9, 9, 0)
    for i in range(9):
        g[4][i] = 9
        g[i][4] = 9
    _paint(g, 0, 0, _A, a_color)
    _paint(g, 0, 5, _A | _ADDS[variant], a_color)
    _paint(g, 5, 0, _Q, q_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_dividers":
        # no color-9 dividers → grid not split into panels, rule has no structure
        _paint(g, 0, 0, _A, 4)
        _paint(g, 0, 5, _A | _ADDS[0], 4)
        _paint(g, 5, 0, _Q, 6)
        return g
    if name == "no_q_panel":
        # bottom-left query panel is empty → rule has no source to paint additions onto
        for i in range(9):
            g[4][i] = 9; g[i][4] = 9
        _paint(g, 0, 0, _A, 4)
        _paint(g, 0, 5, _A | _ADDS[0], 4)
        return g
    if name == "identical_panels":
        # top-left and top-right identical → no additions to extract
        for i in range(9):
            g[4][i] = 9; g[i][4] = 9
        _paint(g, 0, 0, _A, 4)
        _paint(g, 0, 5, _A, 4)
        _paint(g, 5, 0, _Q, 6)
        return g
    return g
