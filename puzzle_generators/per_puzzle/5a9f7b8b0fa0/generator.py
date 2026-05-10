"""Generator for arc_additional_puzzles_21_set20_bundle:H139.

Rule: 8-separated panels are compared by non-background area into an
order matrix.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_count,
palette_size, position_bias, n_distinct_colors, area_spread, texture.
Degenerates: no_separators, equal_areas, single_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "5a9f7b8b0fa0"
VERSION = "1.1.0"
TASK_ID = "5a9f7b8b0fa0"
SUMMARY = "8-separated panels are compared by non-background area into an order matrix."

INVARIANTS = [
    "full color-8 columns split panels",
    "panel scores count cells that are neither 0 nor 8",
    "the output matrix marks equal, greater-than, and less-than area comparisons",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "equal_areas", "single_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "11..14", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_count":    {"type": "int", "default": 3, "range": [3, 4]},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "uniform_panels", "valid": "uniform_panels"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "area_spread":    {"type": "str", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        panel_count = ctx.draw_int("panel_count", 3, 3)
    elif difficulty == "hard":
        panel_count = ctx.draw_int("panel_count", 4, 4)
    else:
        panel_count = ctx.draw_int("panel_count", 3, 4)
    color = ctx.draw_color("color", exclude={0, 8})
    widths = [3] * panel_count
    w = sum(widths) + panel_count - 1
    g = full_grid(5, w, 0)
    left = 0
    for i in range(panel_count):
        if i:
            for r in range(5):
                g[r][left] = 8
            left += 1
        area = 1 + ((sample_index + i * 2) % 5)
        for k in range(area):
            g[1 + (k // 3)][left + (k % 3)] = color
        left += 3
    return g


def _draw_from_degenerate(name, rng):
    if name == "no_separators":
        # one wide panel with no 8-columns → comparison structure absent
        g = full_grid(5, 11, 0)
        for k in range(4):
            g[1 + (k // 3)][1 + (k % 3)] = 4
        for k in range(2):
            g[2 + (k // 2)][6 + (k % 2)] = 4
        return g
    if name == "equal_areas":
        # all panels have same area → comparison matrix is uniform "equal"
        g = full_grid(5, 11, 0)
        left = 0
        for i in range(3):
            if i:
                for r in range(5):
                    g[r][left] = 8
                left += 1
            for k in range(2):
                g[1 + k][left] = 4
            left += 3
        return g
    if name == "single_panel":
        # only one panel → there is nothing to compare against
        g = full_grid(5, 5, 0)
        for k in range(3):
            g[1 + (k // 3)][1 + (k % 3)] = 4
        return g
    return full_grid(5, 11, 0)
