"""Generator for arc_puzzle_bank_twentieth21:H134.

Three 4x4 panels show A, transformed-and-recolored B, and a query C. The
canonical rule infers both the transform and color map from A to B.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers (no color-8 separator columns → rule
cannot identify panels); identity_transform (panel B == panel A
nonzero-support → t = identity); identity_recolor (target colors ==
source colors → no recolor).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0edd8100b9d"
VERSION = "1.1.0"
TASK_ID = "e0edd8100b9d"
SUMMARY = "Infer a 4x4 panel transform plus recolor map and apply it to C."

INVARIANTS = [
    "the input has three 4x4 panels separated by full color-8 columns",
    "panel B is a nonzero-support transform of panel A with a consistent recolor",
    "panel C uses only colors seen in panel A",
    "the output is transformed C recolored by the inferred map",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identity_transform", "identity_recolor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":         {"type": "enum", "default": "rng", "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "position_bias":     {"type": "str", "default": "three_4x4_panels",
                          "valid": "three_4x4_panels"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_A = [(0, 0, 1), (1, 0, 1), (1, 1, 2), (2, 1, 2), (2, 2, 3)]
_C = [(0, 1, 1), (0, 2, 2), (1, 1, 2), (2, 0, 3)]


def _grid_from_cells(cells, colors):
    out = full_grid(4, 4, 0)
    for r, c, slot in cells:
        out[r][c] = colors[slot - 1]
    return out


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
    if code == "fv":
        return list(reversed([row[:] for row in grid]))
    if code == "tr":
        return [[grid[r][c] for r in range(h)] for c in range(w)]
    return [[grid[h - 1 - r][w - 1 - c] for r in range(h - 1, -1, -1)] for c in range(w - 1, -1, -1)]


def _recolor(grid, mapping):
    return [[mapping.get(v, v) for v in row] for row in grid]


def _paste_panel(out, panel, grid):
    left = panel * 5
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            out[r][left + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        codes = ["fh", "fv", "tr"]
    else:
        codes = _CODES
    code = ctx.draw_choice("transform", codes)
    source_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    target_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    mapping = dict(zip(source_colors, target_colors))

    a = _grid_from_cells(_A, source_colors)
    b = _recolor(_xform_grid(a, code), mapping)
    c = _grid_from_cells(_C, source_colors)
    g = full_grid(4, 14, 0)
    for sep in (4, 9):
        for r in range(4):
            g[r][sep] = 8
    _paste_panel(g, 0, a)
    _paste_panel(g, 1, b)
    _paste_panel(g, 2, c)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, 0)
    if name == "no_dividers":
        # No color-8 separators — rule cannot identify panels.
        for r, c, _slot in _A:
            g[r][c] = 4 + (_slot - 1)
        return g
    if name == "identity_transform":
        # Panel B == panel A.
        for sep in (4, 9):
            for r in range(4):
                g[r][sep] = 8
        for r, c, slot in _A:
            color = 4 + (slot - 1)
            g[r][c] = color
            g[r][5 + c] = color
        for r, c, slot in _C:
            g[r][10 + c] = 4 + (slot - 1)
        return g
    if name == "identity_recolor":
        # Source == target colors — no recolor.
        for sep in (4, 9):
            for r in range(4):
                g[r][sep] = 8
        for r, c, slot in _A:
            color = 4 + (slot - 1)
            g[r][c] = color
            g[r][5 + c] = color
        for r, c, slot in _C:
            g[r][10 + c] = 4 + (slot - 1)
        return g
    return g
