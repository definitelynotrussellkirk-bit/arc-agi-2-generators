"""Generator for arc_puzzle_bank_twentyfirst21:H142 — transfer A→B stencil onto query C.

Rule: panel A→B difference (additions and deletions) is applied to
query panel C, where additions get C's color and deletions become 0.

Combinatorial axes (8): variant, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_query, identical_panels, no_separator.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a851bf5cdd7"
VERSION = "1.1.0"
TASK_ID = "8a851bf5cdd7"
SUMMARY = "Transfer a support add/remove stencil from A->B onto query C."

INVARIANTS = [
    "the input has three 3x3 panels separated by full color-8 columns",
    "panel B differs from panel A by at least one deletion and one addition",
    "the query panel has a single nonzero color",
    "additions are painted with the query color and deletions become zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_query", "identical_panels", "no_separator")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_panels_8sep",
                       "valid": "three_panels_8sep"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BEFORE = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
]
_AFTERS = [
    [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 1],
    ],
    [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    [
        [0, 0, 1],
        [1, 1, 0],
        [0, 1, 0],
    ],
]
_QUERY = [
    [0, 5, 0],
    [5, 5, 5],
    [0, 0, 0],
]


def _recolor(grid, one_color):
    return [[one_color if v else 0 for v in row] for row in grid]


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
        variant = ctx.draw_int("variant", 0, 0)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 1, 2)
    else:
        variant = ctx.draw_int("variant", 0, 2)
    base_color = rng.choice([1, 2, 3, 4, 6, 7, 9])
    query_color = rng.choice([4, 5, 6, 7, 9])

    g = full_grid(3, 11, 0)
    for sep in (3, 7):
        for r in range(3):
            g[r][sep] = 8
    panels = [
        _recolor(_BEFORE, base_color),
        _recolor(_AFTERS[variant], base_color),
        _recolor(_QUERY, query_color),
    ]
    for idx, panel in enumerate(panels):
        _paste_panel(g, idx, panel)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 11, 0)
    if name == "no_query":
        # A and B drawn but query panel C is empty — rule has no
        # base shape to apply the stencil to.
        for sep in (3, 7):
            for r in range(3):
                g[r][sep] = 8
        _paste_panel(g, 0, _recolor(_BEFORE, 4))
        _paste_panel(g, 1, _recolor(_AFTERS[0], 4))
        return g
    if name == "identical_panels":
        # A and B identical — no add/remove stencil to transfer.
        for sep in (3, 7):
            for r in range(3):
                g[r][sep] = 8
        _paste_panel(g, 0, _recolor(_BEFORE, 4))
        _paste_panel(g, 1, _recolor(_BEFORE, 4))
        _paste_panel(g, 2, _recolor(_QUERY, 6))
        return g
    if name == "no_separator":
        # Three panels but no 8-separators — panel boundaries undefined.
        _paste_panel(g, 0, _recolor(_BEFORE, 4))
        _paste_panel(g, 1, _recolor(_AFTERS[0], 4))
        _paste_panel(g, 2, _recolor(_QUERY, 6))
        return g
    return g
