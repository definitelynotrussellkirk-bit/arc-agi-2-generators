"""Generator for arc_puzzle_bank_twentythird21:H160.

Replay accent-color stencil positions from A->B onto same-support C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_accent, mismatched_supports, panel_c_already_full.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "170ec3daa52f"
VERSION = "1.1.0"
TASK_ID = "170ec3daa52f"
SUMMARY = "Replay accent-color stencil positions from A->B onto same-support C."

INVARIANTS = [
    "the input has three 4x4 panels separated by full color-8 columns",
    "all panels have the same nonzero support",
    "panel B recolors a few supported cells with one accent color",
    "panel C keeps its base color except at those accent stencil positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_accent", "mismatched_supports", "panel_c_already_full")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..4"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "three_panels_separated_by_8",
                       "valid": "three_panels_separated_by_8"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SUPPORT = {(r, c) for r in range(4) for c in range(4)}
_ACCENTS = [
    [(0, 1), (2, 3)],
    [(1, 0), (1, 2), (3, 2)],
    [(0, 0), (2, 1)],
]


def _paint_panel(g, panel, base_color, accents=(), accent_color=0):
    left = panel * 5
    accent_set = set(accents)
    for r, c in _SUPPORT:
        g[r][left + c] = accent_color if (r, c) in accent_set else base_color


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
    base_a = rng.choice([1, 2, 3, 4])
    accent = rng.choice([6, 7, 9])
    base_c = rng.choice([5, 6, 7, 9])
    g = full_grid(4, 14, 0)
    for sep in (4, 9):
        for r in range(4):
            g[r][sep] = 8
    _paint_panel(g, 0, base_a)
    _paint_panel(g, 1, base_a, _ACCENTS[variant], accent)
    _paint_panel(g, 2, base_c)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 14, 0)
    for sep in (4, 9):
        for r in range(4):
            g[r][sep] = 8
    if name == "no_accent":
        # panels A and B identical → no accent stencil to replay onto C
        _paint_panel(g, 0, 3)
        _paint_panel(g, 1, 3)
        _paint_panel(g, 2, 6)
        return g
    if name == "mismatched_supports":
        # panel C support differs from A/B → "same support" precondition fails
        _paint_panel(g, 0, 3)
        _paint_panel(g, 1, 3, _ACCENTS[0], 7)
        for r in range(4):
            g[r][10] = 6  # only one column on panel C
        return g
    if name == "panel_c_already_full":
        # panel C already has accent everywhere → rule's "stencil onto C" trivial
        _paint_panel(g, 0, 3)
        _paint_panel(g, 1, 3, _ACCENTS[0], 7)
        for r in range(4):
            for c in range(4):
                g[r][10 + c] = 7
        return g
    return g
