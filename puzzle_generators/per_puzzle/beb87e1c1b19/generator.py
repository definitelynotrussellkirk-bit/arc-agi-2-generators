"""Generator for arc_puzzle_bank_twentysecond21:H154 — 3-panel support transform.

Rule: Three 3x3 panels separated by full color-8 columns. Panel B has
the same support as transformed panel A; output overlays panel C with
its own transformed copy (nonzero transformed cells overwrite bg in C).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identity_transform (A==B → 8 valid ops fix A,
transform inference is non-canonical), empty_query (panel C all bg →
overlay has nothing to do), single_cell_panel (panel A has 1 cell →
many transforms produce identical B, ambiguous inference).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "beb87e1c1b19"
VERSION = "1.1.0"
TASK_ID = "beb87e1c1b19"

SUMMARY = "Infer a support transform from A->B and union transformed C with C."

INVARIANTS = [
    "the input has three 3x3 panels separated by full color-8 columns",
    "panel B has the same support as transformed panel A",
    "panel C is overlaid with its own transformed copy",
    "nonzero transformed C cells overwrite background in the original C panel",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_transform", "empty_query", "single_cell_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":      {"type": "enum", "default": "rng",
                       "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_3x3_panels_with_separators",
                       "valid": "three_3x3_panels_with_separators"},
    "n_distinct_colors": {"type": "int", "default": "3..4", "valid": "2..6"},
    "density":        {"type": "str", "default": "fixed_3panel", "valid": "fixed_3panel"},
    "grid_h":         {"type": "int", "default": "3", "valid": "3..3"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_A = [
    [1, 0, 0],
    [1, 1, 0],
    [0, 0, 0],
]
_C = [
    [0, 0, 5],
    [0, 5, 5],
    [0, 0, 0],
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


def _recolor(grid, color):
    return [[color if v else 0 for v in row] for row in grid]


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
        code = ctx.draw_choice("transform", ["fh", "fv", "tr"])
    elif difficulty == "hard":
        code = ctx.draw_choice("transform", _CODES)
    else:
        code = ctx.draw_choice("transform", _CODES)
    a_color = rng.choice([1, 2, 3, 4])
    b_color = rng.choice([2, 3, 4, 6])
    c_color = rng.choice([5, 6, 7, 9])
    a = _recolor(_A, a_color)
    b = _recolor(_xform_grid(_A, code), b_color)
    c = _recolor(_C, c_color)

    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    for idx, panel in enumerate([a, b, c]):
        _paste_panel(g, idx, panel)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    if name == "identity_transform":
        # A and B identical — many transforms map A→A, rule's
        # "infer one transform" branch picks ambiguously.
        a = _recolor(_A, 1)
        c = _recolor(_C, 5)
        for idx, panel in enumerate([a, a, c]):
            _paste_panel(g, idx, panel)
        return g
    if name == "empty_query":
        # Panel C is empty — the "overlay with transformed copy"
        # has no content to overlay; output equals an empty C.
        a = _recolor(_A, 1)
        b = _recolor(_xform_grid(_A, "fh"), 3)
        empty = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for idx, panel in enumerate([a, b, empty]):
            _paste_panel(g, idx, panel)
        return g
    if name == "single_cell_panel":
        # Panel A has just one cell — every rotation/flip maps A→A,
        # transform inference can't distinguish ops.
        a = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
        b = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
        c = _recolor(_C, 5)
        for idx, panel in enumerate([a, b, c]):
            _paste_panel(g, idx, panel)
        return g
    return g
