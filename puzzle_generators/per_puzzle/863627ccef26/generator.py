"""Generator for arc_puzzle_bank_twentieth21:H137 — 3-panel transform infer.

Rule: Three 3x3 panels separated by color-8 columns. Panel B is an exact
transform of panel A; output recovers that transform code and applies it
to panel C, merging C with the transformed copy (overlapping nonzero
cells → 9).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identity_transform (A==B, no info to distinguish ops),
empty_query (panel C all bg, merge has nothing to do),
broken_separators (separator columns not all-8).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "863627ccef26"
VERSION = "1.1.0"
TASK_ID = "863627ccef26"

SUMMARY = "Infer a 3x3 transform, then merge the query with its transformed copy."

INVARIANTS = [
    "the input has three 3x3 panels separated by color-8 columns",
    "panel B is an exact transform of panel A",
    "panel C is merged with its transformed copy by the canonical rule",
    "overlapping nonzero cells become conflict color 9",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_transform", "empty_query", "broken_separators")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "enum", "default": "rng",
                       "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_3x3_panels_with_separators",
                       "valid": "three_3x3_panels_with_separators"},
    "n_distinct_colors": {"type": "int", "default": "3..5", "valid": "2..7"},
    "density":        {"type": "str", "default": "fixed_3panel", "valid": "fixed_3panel"},
    "grid_h":         {"type": "int", "default": "3", "valid": "3..3"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_A = [
    [1, 0, 0],
    [1, 2, 0],
    [0, 0, 3],
]
_Q = [
    [4, 4, 0],
    [4, 0, 0],
    [0, 0, 6],
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
    left = panel * 4
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
        # Restrict to most-distinguishable transforms.
        code = ctx.draw_choice("transform", ["fh", "fv", "tr"])
    elif difficulty == "hard":
        code = ctx.draw_choice("transform", _CODES)
    else:
        code = ctx.draw_choice("transform", _CODES)
    mapping = {1: rng.choice([1, 2]), 2: rng.choice([3, 4]), 3: rng.choice([5, 6, 7])}
    q_mapping = {4: rng.choice([2, 4, 5]), 6: rng.choice([6, 7])}
    a = _recolor(_A, mapping)
    b = _xform_grid(a, code)
    q = _recolor(_Q, q_mapping)

    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    for idx, panel in enumerate([a, b, q]):
        _paste_panel(g, idx, panel)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    if name == "identity_transform":
        # B = A — rule's transform inference has 8 valid candidates
        # (every op that fixes A); selection is non-canonical.
        for idx, panel in enumerate([_A, _A, _Q]):
            _paste_panel(g, idx, panel)
        return g
    if name == "empty_query":
        # Panel C is all zero — rule's "merge with transformed copy"
        # has nothing non-bg to merge; output equals C trivially.
        empty = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        b = _xform_grid(_A, "fh")
        for idx, panel in enumerate([_A, b, empty]):
            _paste_panel(g, idx, panel)
        return g
    if name == "broken_separators":
        # Separator columns are not uniform 8 — rule's panel
        # extraction (split on color-8 columns) finds a different
        # decomposition than the canonical 3x3 split.
        for idx, panel in enumerate([_A, _xform_grid(_A, "fh"), _Q]):
            _paste_panel(g, idx, panel)
        # Knock out one separator cell.
        g[1][3] = 0
        return g
    return g
