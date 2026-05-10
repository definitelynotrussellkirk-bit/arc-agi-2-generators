"""Generator for arc_puzzle_bank_twentythird21:H155 — header-color recolors transformed C.

Read a header color, infer a transform, then recolor transformed C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identity_transform (A==B → 8 ops fix A; transform
inference is non-canonical), no_header (cell (0,0) is bg → recolor
target undefined), empty_query (panel C all bg → output's recolor
has nothing to paint).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a2afa3c0d4b"
VERSION = "1.1.0"
TASK_ID = "1a2afa3c0d4b"
SUMMARY = "Read a header color, infer a transform, then recolor transformed C."

INVARIANTS = [
    "row 0 contains the output recolor target as its first nonzero cell",
    "rows 1-4 contain three 4x4 panels split by full color-8 columns",
    "panel B is an exact transform of panel A",
    "the transformed third panel is recolored uniformly by the header color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_transform", "no_header", "empty_query")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "enum", "default": "rng", "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "header_plus_three_panels",
                       "valid": "header_plus_three_panels"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_A = [
    [1, 1, 0, 0],
    [0, 1, 2, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 0],
]
_C = [
    [3, 0, 0, 0],
    [3, 3, 3, 0],
    [0, 0, 0, 0],
    [0, 4, 0, 0],
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
            out[1 + r][left + c] = value


def _make_separators(g):
    for sep in (4, 9):
        for r in range(1, 5):
            g[r][sep] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    code = ctx.draw_choice("transform", _CODES)
    target = rng.choice([2, 3, 4, 5, 6, 7, 9])
    mapping = {1: rng.choice([1, 2, 3]), 2: rng.choice([4, 5, 6])}
    q_mapping = {3: rng.choice([2, 3, 5]), 4: rng.choice([6, 7, 9])}
    a = _recolor(_A, mapping)
    b = _xform_grid(a, code)
    c = _recolor(_C, q_mapping)

    g = full_grid(5, 14, 0)
    g[0][0] = target
    _make_separators(g)
    for idx, panel in enumerate([a, b, c]):
        _paste_panel(g, idx, panel)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 14, 0)
    _make_separators(g)
    if name == "identity_transform":
        # A == B → 8 ops fix A; rule's transform inference can't
        # pick a unique transform.
        a = _recolor(_A, {1: 2, 2: 4})
        c = _recolor(_C, {3: 5, 4: 6})
        g[0][0] = 7
        for idx, panel in enumerate([a, a, c]):
            _paste_panel(g, idx, panel)
        return g
    if name == "no_header":
        # Cell (0,0) is bg — rule's recolor target undefined.
        a = _recolor(_A, {1: 2, 2: 4})
        b = _xform_grid(a, "fh")
        c = _recolor(_C, {3: 5, 4: 6})
        for idx, panel in enumerate([a, b, c]):
            _paste_panel(g, idx, panel)
        return g
    if name == "empty_query":
        # Panel C all bg — rule's recolor has nothing to paint.
        a = _recolor(_A, {1: 2, 2: 4})
        b = _xform_grid(a, "fh")
        empty = [[0, 0, 0, 0]] * 4
        g[0][0] = 7
        for idx, panel in enumerate([a, b, empty]):
            _paste_panel(g, idx, panel)
        return g
    return g
