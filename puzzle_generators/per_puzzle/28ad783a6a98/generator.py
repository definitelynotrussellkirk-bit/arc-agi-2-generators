"""Generator for arc_puzzle_bank_twentythird21:H161 — compose two 4x4 transforms on 5th panel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identity_first (panel 1 == panel 2 → t1 is identity),
identity_second (panel 3 == panel 4 → t2 is identity), no_dividers
(no color-8 separators → rule's 5-panel split fails).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28ad783a6a98"
VERSION = "1.1.0"
TASK_ID = "28ad783a6a98"
SUMMARY = "Infer two 4x4 transforms and compose them on the fifth panel."

INVARIANTS = [
    "the input has five 4x4 panels separated by full color-8 columns",
    "panel 2 is an exact transform of panel 1",
    "panel 4 is an exact transform of panel 3",
    "the canonical rule applies transform 1 then transform 2 to panel 5",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_first", "identity_second", "no_dividers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "first_transform":   {"type": "enum", "default": "rng",
                          "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "second_transform":  {"type": "enum", "default": "rng",
                          "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "five_panels_two_transforms",
                          "valid": "five_panels_two_transforms"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_A = [
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]
_C = [
    [2, 2, 0, 0],
    [2, 2, 2, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 0],
]
_X = [
    [3, 3, 0, 0],
    [0, 3, 0, 0],
    [0, 3, 0, 0],
    [0, 0, 0, 0],
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
    t1 = ctx.draw_choice("first_transform", _CODES)
    t2 = ctx.draw_choice("second_transform", _CODES)
    mapping = {1: rng.choice([1, 2, 4]), 2: rng.choice([3, 5, 6]), 3: rng.choice([4, 7, 9])}
    a = _recolor(_A, mapping)
    c = _recolor(_C, mapping)
    x = _recolor(_X, mapping)
    panels = [a, _xform_grid(a, t1), c, _xform_grid(c, t2), x]

    g = full_grid(4, 24, 0)
    for sep in (4, 9, 14, 19):
        for r in range(4):
            g[r][sep] = 8
    for idx, panel in enumerate(panels):
        _paste_panel(g, idx, panel)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 24, 0)
    def fill_dividers():
        for sep in (4, 9, 14, 19):
            for r in range(4):
                g[r][sep] = 8
    if name == "identity_first":
        # Panel 1 == Panel 2 → t1 is identity.
        fill_dividers()
        _paste_panel(g, 0, _A)
        _paste_panel(g, 1, _A)   # identity
        _paste_panel(g, 2, _C)
        _paste_panel(g, 3, _xform_grid(_C, "r1"))
        _paste_panel(g, 4, _X)
        return g
    if name == "identity_second":
        # Panel 3 == Panel 4 → t2 is identity.
        fill_dividers()
        _paste_panel(g, 0, _A)
        _paste_panel(g, 1, _xform_grid(_A, "fh"))
        _paste_panel(g, 2, _C)
        _paste_panel(g, 3, _C)   # identity
        _paste_panel(g, 4, _X)
        return g
    if name == "no_dividers":
        # No color-8 separators — rule's 5-panel split fails.
        _paste_panel(g, 0, _A)
        _paste_panel(g, 1, _xform_grid(_A, "fh"))
        _paste_panel(g, 2, _C)
        _paste_panel(g, 3, _xform_grid(_C, "r1"))
        _paste_panel(g, 4, _X)
        return g
    return g
