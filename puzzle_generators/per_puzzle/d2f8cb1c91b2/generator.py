"""Generator for arc_puzzle_bank_nineteenth21:H132 — panel-transform conflict-merge.

The first two panels identify a geometric transform. The same transform
is applied to the third panel and merged with the fourth panel, with
conflicts marked as color 9 by the canonical rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers (no color-5 dividers → rule's panel selector
returns nothing), identity_transform (panel 2 == panel 1 → rule's
inferred transform is identity, no conflict resolution needed),
no_conflict (panels 3 and 4 have no overlap → rule's color-9
conflict-marker never fires).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d2f8cb1c91b2"
VERSION = "1.1.0"
TASK_ID = "d2f8cb1c91b2"
SUMMARY = "Infer a transform from two panels, then conflict-merge a transformed query."

INVARIANTS = [
    "the input has four 3x3 panels separated by color-5 columns",
    "panel 2 is an exact color-preserving transform of panel 1",
    "panels 3 and 4 have at least one overlapping nonzero conflict",
    "the output keeps lone cells and matching overlaps, using 9 for conflicts",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identity_transform", "no_conflict")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "transform":         {"type": "enum", "default": "rng",
                          "valid": "r1|r2|r3|fh|fv|tr|atr"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "position_bias":     {"type": "str", "default": "four_panels_with_dividers",
                          "valid": "four_panels_with_dividers"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = ["r1", "r2", "r3", "fh", "fv", "tr", "atr"]
_EXAMPLE = [
    [1, 0, 0],
    [1, 2, 0],
    [0, 0, 3],
]
_X = [
    [0, 4, 0],
    [4, 4, 0],
    [0, 0, 6],
]
_Y_VARIANTS = [
    [
        [0, 0, 0],
        [0, 4, 7],
        [0, 0, 6],
    ],
    [
        [0, 8, 0],
        [0, 0, 7],
        [6, 0, 0],
    ],
    [
        [0, 0, 7],
        [4, 0, 0],
        [0, 6, 0],
    ],
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


def _recolor_grid(grid, mapping):
    return [[mapping.get(v, v) for v in row] for row in grid]


def _paste_panel(out, panel, grid):
    left = panel * 4
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            out[r][left + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    code = ctx.draw_choice("transform", _CODES)
    y = rng.choice(_Y_VARIANTS)
    mapping = {1: rng.choice([1, 2, 3]), 2: rng.choice([4, 5, 6]), 3: rng.choice([6, 7, 8])}
    x_mapping = {4: rng.choice([2, 3, 4]), 6: rng.choice([6, 7, 8])}

    ex_in = _recolor_grid(_EXAMPLE, mapping)
    ex_out = _xform_grid(ex_in, code)
    x = _recolor_grid(_X, x_mapping)

    g = full_grid(3, 15, 0)
    for sep in (3, 7, 11):
        for r in range(3):
            g[r][sep] = 5
    for idx, panel in enumerate([ex_in, ex_out, x, y]):
        _paste_panel(g, idx, panel)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 15, 0)
    # Helper to paste a 3x3 panel
    def paste(idx, panel):
        left = idx * 4
        for r in range(3):
            for c in range(3):
                g[r][left + c] = panel[r][c]
    if name == "no_dividers":
        # No color-5 dividers — rule's panel selector finds no separators.
        paste(0, _EXAMPLE)
        paste(1, _EXAMPLE)   # identity (no transform inferred)
        paste(2, _X)
        paste(3, _Y_VARIANTS[0])
        return g
    if name == "identity_transform":
        # Panel 2 == Panel 1 — inferred transform is identity.
        for sep in (3, 7, 11):
            for r in range(3):
                g[r][sep] = 5
        paste(0, _EXAMPLE)
        paste(1, _EXAMPLE)
        paste(2, _X)
        paste(3, _Y_VARIANTS[0])
        return g
    if name == "no_conflict":
        # Panels 3 and 4 have no overlap — color-9 marker never fires.
        for sep in (3, 7, 11):
            for r in range(3):
                g[r][sep] = 5
        paste(0, _EXAMPLE)
        paste(1, _xform_grid(_EXAMPLE, "fh"))
        paste(2, [[4, 0, 0], [0, 0, 0], [0, 0, 0]])
        paste(3, [[0, 0, 0], [0, 0, 0], [0, 0, 6]])   # disjoint
        return g
    return g
