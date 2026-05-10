"""Generator for arc_puzzle_bank_twentythird21:M158.

Combinatorial axes (8): grid_h, grid_w, palette_kind, transform,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_panel_a, no_panel_b, identical_a_b.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "53de1fcb2e13"
VERSION = "1.1.0"
TASK_ID = "53de1fcb2e13"
SUMMARY = "Infer a panel transform from A to B, then apply it to C."

INVARIANTS = [
    "three 4x4 panels are separated by full color-8 columns",
    "panel B is an exact geometric transform of panel A",
    "panel C is transformed by the same operation",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_panel_a", "no_panel_b", "identical_a_b")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "transform":      {"type": "int", "default": "rng 1..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_panels_with_transform",
                       "valid": "three_panels_with_transform"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_A = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
_C = [(0, 0), (1, 0), (1, 2), (2, 2), (3, 1)]


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
    n = 4
    if difficulty == "easy":
        code = ctx.draw_int("transform", 1, 2)
    elif difficulty == "hard":
        code = ctx.draw_int("transform", 3, 5)
    else:
        code = ctx.draw_int("transform", 1, 5)
    g = full_grid(n, n * 3 + 2, 0)
    for r in range(n):
        g[r][n] = 8
        g[r][2 * n + 1] = 8
    _paint(g, 0, _A, 2)
    _paint(g, n + 1, _xform(_A, n, code), 2)
    _paint(g, 2 * n + 2, _C, 4)
    return g


def _draw_from_degenerate(name, rng):
    n = 4
    g = full_grid(n, n * 3 + 2, 0)
    for r in range(n):
        g[r][n] = 8
        g[r][2 * n + 1] = 8
    if name == "no_panel_a":
        # A panel empty → no source for transform
        _paint(g, n + 1, _xform(_A, n, 1), 2)
        _paint(g, 2 * n + 2, _C, 4)
        return g
    if name == "no_panel_b":
        # B panel empty → no transform demonstration
        _paint(g, 0, _A, 2)
        _paint(g, 2 * n + 2, _C, 4)
        return g
    if name == "identical_a_b":
        # A and B identical → transform is identity (no signal for what to do to C)
        _paint(g, 0, _A, 2)
        _paint(g, n + 1, _A, 2)
        _paint(g, 2 * n + 2, _C, 4)
        return g
    return g
