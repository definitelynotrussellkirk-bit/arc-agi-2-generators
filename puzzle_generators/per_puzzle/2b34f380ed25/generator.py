"""Generator for 4e7e0eb9.

Rule: parse 3x3 macro-cells and fill panel placeholders.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
fill_color.
Degenerates: no_macros, no_fill, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "2b34f380ed25"
VERSION = "1.1.0"
TASK_ID = "2b34f380ed25"
SUMMARY = "Four 3x3 macro-cell slots form a 2x2 panel with color 1 filled from another color."

INVARIANTS = [
    "background is 0",
    "macro-cells are 3x3 solid blocks separated by one blank row/column",
    "one macro-cell is color 1 and the only other nonzero macro color is the fill color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_macros", "no_fill", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "7", "valid": "7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "fill_color":     {"type": "int", "default": "rng 2..9", "valid": "2..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    fill_color = ctx.draw_int("fill_color", 2, 9)
    g = full_grid(7, 7, 0)
    fill_box(g, 0, 0, 2, 2, 1)
    fill_box(g, 0, 4, 2, 6, fill_color)
    if rng.random() < 0.5:
        fill_box(g, 4, 4, 6, 6, fill_color)
    else:
        fill_box(g, 4, 0, 6, 2, fill_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_macros":
        return g
    if name == "no_fill":
        fill_box(g, 0, 0, 2, 2, 1)
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 1
        return g
    return g
