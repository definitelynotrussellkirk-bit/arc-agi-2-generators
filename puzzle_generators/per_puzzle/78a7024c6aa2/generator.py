"""Generator for arc_puzzle_bank_fourteenth21:H92.

Rule: infer a whole-panel transform from top pair, apply to bottom-left.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, identical_top_panels, no_query.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "78a7024c6aa2"
VERSION = "1.1.0"
TASK_ID = "78a7024c6aa2"
SUMMARY = "Infer a whole-panel transform and fill the blank lower-right panel."

INVARIANTS = [
    "the grid is split into four 3x3 panels by color-9 separators",
    "top-right is a transform of top-left",
    "bottom-left is the query panel",
    "bottom-right is blank until the rule writes transformed query cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "identical_top_panels", "no_query")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "enum", "default": "rng", "valid": "r1|r2|r3|fh|fv"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "2x2_panel_grid",
                       "valid": "2x2_panel_grid"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv"]
_A = [
    [1, 1, 0],
    [1, 0, 0],
    [0, 0, 0],
]
_Q = [
    [2, 2, 0],
    [0, 2, 0],
    [0, 2, 0],
]


def _xform_grid(grid, code):
    h = len(grid)
    w = len(grid[0])
    if code == "r1":
        return [[grid[h - 1 - r][c] for r in range(h)] for c in range(w)]
    if code == "r2":
        return [[grid[h - 1 - r][w - 1 - c] for c in range(w)] for r in range(h)]
    if code == "r3":
        return [[grid[r][w - 1 - c] for r in range(h)] for c in range(w - 1, -1, -1)]
    if code == "fh":
        return [list(reversed(row)) for row in grid]
    return list(reversed([row[:] for row in grid]))


def _recolor(grid, mapping):
    return [[mapping.get(v, v) for v in row] for row in grid]


def _paste(g, top, left, panel):
    for r, row in enumerate(panel):
        for c, value in enumerate(row):
            g[top + r][left + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    code = ctx.draw_choice("transform", _CODES)
    mapping = {1: rng.choice([1, 2, 4]), 2: rng.choice([3, 5, 6, 7])}
    a = _recolor(_A, mapping)
    q = _recolor(_Q, mapping)

    g = full_grid(7, 7, 0)
    for i in range(7):
        g[3][i] = 9
        g[i][3] = 9
    _paste(g, 0, 0, a)
    _paste(g, 0, 4, _xform_grid(a, code))
    _paste(g, 4, 0, q)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_separators":
        # No 9-dividers — rule's panel decomposition fails.
        _paste(g, 0, 0, _A)
        _paste(g, 0, 4, _A)
        _paste(g, 4, 0, _Q)
        return g
    for i in range(7):
        g[3][i] = 9
        g[i][3] = 9
    if name == "identical_top_panels":
        # Top-left and top-right identical — inferred transform is
        # identity; rule's effect is invisible.
        _paste(g, 0, 0, _A)
        _paste(g, 0, 4, _A)
        _paste(g, 4, 0, _Q)
        return g
    if name == "no_query":
        # Top pair shows transform but bottom-left empty — rule
        # has nothing to apply the transform to.
        _paste(g, 0, 0, _A)
        _paste(g, 0, 4, _xform_grid(_A, "fh"))
        return g
    return g
