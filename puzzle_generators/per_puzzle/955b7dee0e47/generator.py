"""Generator for arc_puzzle_bank_twentythird21:H156 — replay A→B edit onto C.

Rule: crop A, B, C and replay the relative support edit A->B onto C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_panel_a, identical_a_b.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "955b7dee0e47"
VERSION = "1.1.0"
TASK_ID = "955b7dee0e47"
SUMMARY = "Crop A, B, C and replay the relative support edit A->B onto C."

INVARIANTS = [
    "the input has three 4x4 panels separated by full color-8 columns",
    "cropped A, B, and C have matching dimensions",
    "A->B contains both a relative deletion and a relative addition",
    "the output uses C's dominant color on the edited support",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_panel_a", "identical_a_b")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
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


def _paint_panel(g, panel, cells, color):
    left = panel * 5
    for r, c in cells:
        g[r][left + c] = color


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

    g = full_grid(4, 14, 0)
    for sep in (4, 9):
        for r in range(4):
            g[r][sep] = 8
    _paint_panel(g, 0, _A, a_color)
    _paint_panel(g, 1, _B_VARIANTS[variant], a_color)
    _paint_panel(g, 2, _C, c_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, 0)
    if name == "no_separators":
        # panels exist but no 8-column separators → cannot crop A/B/C
        _paint_panel(g, 0, _A, 4)
        _paint_panel(g, 1, _B_VARIANTS[0], 4)
        _paint_panel(g, 2, _C, 6)
        return g
    if name == "no_panel_a":
        # B and C present, separators present, but A panel is empty → no A→B edit
        for sep in (4, 9):
            for r in range(4):
                g[r][sep] = 8
        _paint_panel(g, 1, _B_VARIANTS[0], 4)
        _paint_panel(g, 2, _C, 6)
        return g
    if name == "identical_a_b":
        # A == B → no edit to replay; rule produces an unchanged C
        for sep in (4, 9):
            for r in range(4):
                g[r][sep] = 8
        _paint_panel(g, 0, _A, 4)
        _paint_panel(g, 1, _A, 4)   # B = A
        _paint_panel(g, 2, _C, 6)
        return g
    return g
