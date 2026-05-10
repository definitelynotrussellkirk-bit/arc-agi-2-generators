"""Generator for arc_puzzle_bank_21_set12_s:S12_H2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, odd_panel, odd_shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, all_same, no_odd.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c60ba52071ec"
VERSION = "1.1.0"
TASK_ID = "c60ba52071ec"
SUMMARY = "Find the odd separator-delimited panel by graph degree multiset and crop its cluster."

INVARIANTS = [
    "two full color-5 columns split the grid into three panels",
    "two panels contain a three-component contact chain with degree pattern [1,1,2]",
    "one panel contains a four-component contact chain with degree pattern [1,1,2,2]",
    "the output is the odd panel's contact cluster recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "all_same", "no_odd")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "26", "valid": "26..26"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "odd_panel":      {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "odd_shape":      {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "3_panels_with_one_odd_chain",
                       "valid": "3_panels_with_one_odd_chain"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_ODD_CHAINS = [
    [(3, 0), (3, 2), (3, 4), (3, 6)],
    [(0, 3), (2, 3), (4, 3), (6, 3)],
    [(1, 1), (1, 3), (3, 3), (3, 5)],
]


def _block(g, top, left, color):
    for r in range(2):
        for c in range(2):
            g[top + r][left + c] = color


def _paint_chain(g, panel_left, starts, colors):
    for (top, left), color in zip(starts, colors):
        _block(g, top, panel_left + left, color)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        odd_panel = ctx.draw_int("odd_panel", 0, 1)
        odd_shape = ctx.draw_int("odd_shape", 0, 1)
    elif difficulty == "hard":
        odd_panel = ctx.draw_int("odd_panel", 1, 2)
        odd_shape = ctx.draw_int("odd_shape", 1, 2)
    else:
        odd_panel = ctx.draw_int("odd_panel", 0, 2)
        odd_shape = ctx.draw_int("odd_shape", 0, len(_ODD_CHAINS) - 1)
    g = full_grid(8, 26, 0)
    for r in range(8):
        g[r][8] = 5
        g[r][17] = 5
    panel_lefts = [0, 9, 18]
    for idx, left in enumerate(panel_lefts):
        colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 4)
        if idx == odd_panel:
            _paint_chain(g, left, _ODD_CHAINS[odd_shape], colors)
        else:
            _paint_chain(g, left, [(3, 1), (3, 3), (3, 5)], colors[:3])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 26, 0)
    if name == "no_dividers":
        # chains but no 5-divider columns → no panel boundaries
        for left in [0, 9, 18]:
            _paint_chain(g, left, [(3, 1), (3, 3), (3, 5)], [4, 6, 7])
        return g
    if name == "all_same":
        # all 3 panels have identical chain → no odd panel
        for r in range(8):
            g[r][8] = 5; g[r][17] = 5
        for left in [0, 9, 18]:
            _paint_chain(g, left, [(3, 1), (3, 3), (3, 5)], [4, 6, 7])
        return g
    if name == "no_odd":
        # 2 panels normal, 1 empty → can't tell odd from absent
        for r in range(8):
            g[r][8] = 5; g[r][17] = 5
        for left in [0, 9]:
            _paint_chain(g, left, [(3, 1), (3, 3), (3, 5)], [4, 6, 7])
        return g
    return g
