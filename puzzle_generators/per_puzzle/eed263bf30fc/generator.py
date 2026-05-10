"""Generator for arc_puzzle_bank_thirteenth21:H85.

Rule: infer a quadrant transform from top panels and apply to bottom-left.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, identical_top_panels, no_query.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "eed263bf30fc"
VERSION = "1.1.0"
TASK_ID = "eed263bf30fc"
SUMMARY = "Infer a quadrant transform from top panels and apply it to bottom-left."

INVARIANTS = [
    "the 7x7 grid is split by a full color-9 row and column",
    "the top-right panel is a transform of the top-left panel",
    "the bottom-right panel starts blank",
    "the canonical rule pastes the same transform of the bottom-left panel",
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
    [0, 1, 0],
    [0, 0, 0],
]
_Q = [
    [2, 0, 0],
    [2, 2, 0],
    [2, 0, 0],
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
        # Top-left == top-right — inferred transform is identity;
        # rule's transform branch has no visible effect on query.
        _paste(g, 0, 0, _A)
        _paste(g, 0, 4, _A)
        _paste(g, 4, 0, _Q)
        return g
    if name == "no_query":
        # Top pair shows transform but bottom-left empty —
        # rule has nothing to apply the transform to.
        _paste(g, 0, 0, _A)
        _paste(g, 0, 4, _xform_grid(_A, "r2"))
        return g
    return g
