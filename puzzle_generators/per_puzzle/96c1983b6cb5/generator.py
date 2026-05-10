"""Generator for arc_puzzle_bank_twentysecond21:M149.

Panels A and B demonstrate a geometric transform. The same transform should be
applied to panel C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, transform,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, identical_AB, no_C.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "96c1983b6cb5"
VERSION = "1.1.0"
TASK_ID = "96c1983b6cb5"
SUMMARY = "Infer the exact A-to-B transform and apply it to C."

INVARIANTS = [
    "three square panels are separated by full color-8 columns",
    "panel B is an exact transform of panel A",
    "panel C uses a different color but the same transform family",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identical_AB", "no_C")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "transform":      {"type": "int", "default": "rng 1..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "abc_panels_8col_separated",
                       "valid": "abc_panels_8col_separated"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_A = [(0, 0), (1, 0), (1, 1), (2, 1)]
_C = [(0, 1), (0, 2), (1, 2), (2, 0)]


def _xform(cells, n, code):
    if code == 0:
        return list(cells)
    if code == 1:
        return [(r, n - 1 - c) for r, c in cells]
    if code == 2:
        return [(n - 1 - r, c) for r, c in cells]
    if code == 3:
        return [(c, n - 1 - r) for r, c in cells]
    if code == 4:
        return [(n - 1 - r, n - 1 - c) for r, c in cells]
    return [(n - 1 - c, r) for r, c in cells]


def _paint(g, left, cells, color):
    for r, c in cells:
        g[r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("panel_size", 3, 3)
        code = ctx.draw_int("transform", 1, 2)
    elif difficulty == "hard":
        n = ctx.draw_int("panel_size", 4, 4)
        code = ctx.draw_int("transform", 1, 5)
    else:
        n = ctx.draw_int("panel_size", 3, 4)
        code = ctx.draw_int("transform", 1, 5)
    g = full_grid(n, n * 3 + 2, 0)
    for r in range(n):
        g[r][n] = 8
        g[r][2 * n + 1] = 8
    _paint(g, 0, _A, 2)
    _paint(g, n + 1, _xform(_A, n, code), 2)
    _paint(g, 2 * n + 2, _C, 3)
    return g


def _draw_from_degenerate(name, rng):
    n = 3
    g = full_grid(n, n * 3 + 2, 0)
    if name == "no_dividers":
        # missing 8-cols → can't separate A/B/C
        _paint(g, 0, _A, 2)
        _paint(g, n + 1, _xform(_A, n, 2), 2)
        _paint(g, 2 * n + 2, _C, 3)
        return g
    if name == "identical_AB":
        # A == B → identity transform, no signal to learn
        for r in range(n):
            g[r][n] = 8; g[r][2 * n + 1] = 8
        _paint(g, 0, _A, 2)
        _paint(g, n + 1, _A, 2)  # identity
        _paint(g, 2 * n + 2, _C, 3)
        return g
    if name == "no_C":
        # A→B demo but no C operand → no target to apply transform to
        for r in range(n):
            g[r][n] = 8; g[r][2 * n + 1] = 8
        _paint(g, 0, _A, 2)
        _paint(g, n + 1, _xform(_A, n, 2), 2)
        return g
    return g
