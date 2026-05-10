"""Generator for arc_additional_puzzle_bank_volume7:H49.

Rule: top two rows hold label-to-fill pairs (label in row 0, fill in
row 1). Below that, gray walls separate chambers; each chamber's
single label cell selects the fill color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, label_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_walls, label_unmatched.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2d08d999e513"
VERSION = "1.1.0"
TASK_ID = "2d08d999e513"
SUMMARY = "Top-row legend + two gray-walled chambers each holding one label."

INVARIANTS = [
    "top two rows contain nonzero label-to-fill pairs",
    "below row 2, gray walls separate chambers",
    "each chamber contains exactly one label cell",
    "chamber backgrounds are blank before filling",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_walls", "label_unmatched")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "label_count":    {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "top_legend_walled_chambers",
                       "valid": "top_legend_walled_chambers"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "density":        {"type": "str", "default": "walled", "valid": "walled"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _carve(g, r0, c0, r1, c1):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            g[r][c] = 0


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 11, 16)
    g = full_grid(h, w, 0)
    g[0][0], g[1][0] = 1, 6
    g[0][1], g[1][1] = 2, 7
    for r in range(2, h):
        for c in range(w):
            g[r][c] = 5
    mid = w // 2
    _carve(g, 3, 1, h - 2, mid - 1)
    _carve(g, 3, mid + 1, h - 2, w - 2)
    g[4][2] = 1
    g[4][mid + 2] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # walls + chambers with labels but no top-row legend → fill colors undefined
        for r in range(2, h):
            for c in range(w):
                g[r][c] = 5
        mid = w // 2
        _carve(g, 3, 1, h - 2, mid - 1)
        _carve(g, 3, mid + 1, h - 2, w - 2)
        g[4][2] = 1
        g[4][mid + 2] = 2
        return g
    if name == "no_walls":
        # legend present but the chamber walls are missing → no chambers to fill
        g[0][0], g[1][0] = 1, 6
        g[0][1], g[1][1] = 2, 7
        g[4][2] = 1
        g[4][8] = 2
        return g
    if name == "label_unmatched":
        # chamber holds a label that isn't in the legend → no fill mapping
        g[0][0], g[1][0] = 1, 6
        g[0][1], g[1][1] = 2, 7
        for r in range(2, h):
            for c in range(w):
                g[r][c] = 5
        mid = w // 2
        _carve(g, 3, 1, h - 2, mid - 1)
        _carve(g, 3, mid + 1, h - 2, w - 2)
        g[4][2] = 4  # unknown label
        g[4][mid + 2] = 9  # unknown label
        return g
    return g
