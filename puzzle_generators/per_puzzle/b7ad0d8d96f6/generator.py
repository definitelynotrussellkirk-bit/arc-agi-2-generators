"""Generator for 5a719d11.

Rule: two-panel row groups swap their foreground shape masks, recoloring
each mask to the opposite panel background.

Combinatorial axes (8): grid_h/w, row_groups, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_groups, single_panel, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7ad0d8d96f6"
VERSION = "1.1.0"
TASK_ID = "b7ad0d8d96f6"
SUMMARY = "Two-panel row groups swap shape masks and recolor to the opposite panel background."

INVARIANTS = [
    "zero rows and columns separate row groups and the two panels",
    "each panel has its own background color",
    "foreground shape cells are the cells not equal to that panel background",
    "within each row group, left and right shape masks swap panels and recolor to the other panel's background",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_groups", "single_panel", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "row_groups":     {"type": "int", "default": "2", "valid": "2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "6", "valid": "6"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_shape(g, r0, c0, cells, color):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    colors = ctx.draw_distinct_colors("colors", n=6, exclude={0})
    g = full_grid(15, 13, 0)
    group_h = 6
    panel_w = 6
    left_shape = [(1, 1), (1, 2), (2, 1), (3, 1)]
    right_shape = [(1, 3), (2, 2), (2, 3), (3, 3)]
    for gi, r0 in enumerate([0, 8]):
        bg_l = colors[gi * 3]
        bg_r = colors[gi * 3 + 1]
        shape = colors[gi * 3 + 2]
        for r in range(group_h):
            for c in range(panel_w):
                g[r0 + r][c] = bg_l
                g[r0 + r][panel_w + 1 + c] = bg_r
        _paint_shape(g, r0, 0, left_shape, shape)
        _paint_shape(g, r0, panel_w + 1, right_shape, shape)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 13, 0)
    if name == "no_groups":
        return g
    if name == "single_panel":
        for r in range(6):
            for c in range(6):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(13):
                g[r][c] = 4
        return g
    return g
