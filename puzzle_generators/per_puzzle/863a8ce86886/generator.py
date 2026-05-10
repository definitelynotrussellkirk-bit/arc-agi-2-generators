"""Generator for arc_puzzle_bank_twentysecond21:H149 — replay relative A→B edit onto C.

Rule: transfer a relative support add/remove edit from A->B onto C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_panel_a, identical_a_b.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "863a8ce86886"
VERSION = "1.1.0"
TASK_ID = "863a8ce86886"
SUMMARY = "Transfer a relative support add/remove edit from A->B onto C."

INVARIANTS = [
    "the input has three 5x5 panels separated by full color-8 columns",
    "panels A and B share a 3x3 edit bbox",
    "panel C has the same-size bbox at another position",
    "relative deletions clear C cells and relative additions use C's color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_panel_a", "identical_a_b")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5..5"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_panels_with_separators",
                       "valid": "three_panels_with_separators"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_A = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)}
_B_VARIANTS = [
    {(0, 0), (1, 1), (2, 1), (2, 2)},
    {(0, 1), (1, 0), (1, 1), (2, 0), (2, 2)},
    {(0, 0), (0, 2), (1, 1), (2, 2)},
]
_C = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)}


def _paint_cells(g, panel, top, left, cells, color):
    base = panel * 6
    for r, c in cells:
        g[top + r][base + left + c] = color


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
    a_color = rng.choice([1, 2, 3, 4])
    c_color = rng.choice([5, 6, 7, 9])

    g = full_grid(5, 17, 0)
    for sep in (5, 11):
        for r in range(5):
            g[r][sep] = 8
    _paint_cells(g, 0, 1, 1, _A, a_color)
    _paint_cells(g, 1, 1, 1, _B_VARIANTS[variant], a_color)
    _paint_cells(g, 2, 0, 2, _C, c_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 17, 0)
    if name == "no_separators":
        # panels exist but no 8-separators → cannot crop A/B/C
        _paint_cells(g, 0, 1, 1, _A, 4)
        _paint_cells(g, 1, 1, 1, _B_VARIANTS[0], 4)
        _paint_cells(g, 2, 0, 2, _C, 6)
        return g
    if name == "no_panel_a":
        # B and C present + separators but A panel is empty → no A→B edit
        for sep in (5, 11):
            for r in range(5):
                g[r][sep] = 8
        _paint_cells(g, 1, 1, 1, _B_VARIANTS[0], 4)
        _paint_cells(g, 2, 0, 2, _C, 6)
        return g
    if name == "identical_a_b":
        # A == B → edit is empty, rule produces unchanged C
        for sep in (5, 11):
            for r in range(5):
                g[r][sep] = 8
        _paint_cells(g, 0, 1, 1, _A, 4)
        _paint_cells(g, 1, 1, 1, _A, 4)   # B = A
        _paint_cells(g, 2, 0, 2, _C, 6)
        return g
    return g
