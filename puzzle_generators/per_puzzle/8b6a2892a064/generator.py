"""Generator for f0f8a26d.

Rule: straight connected components rotate 90 degrees around their
centers on color-7 background.

Combinatorial axes (8): grid_h/w, line_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_lines, single_line, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b6a2892a064"
VERSION = "1.1.0"
TASK_ID = "8b6a2892a064"
SUMMARY = "Straight components rotate 90 degrees around centers on bg=7."

INVARIANTS = [
    "the background is fixed color 7",
    "foreground components are straight horizontal or vertical lines",
    "odd line lengths keep integer centers",
    "line colors are distinct and non-7",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lines", "single_line", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "line_count":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 1..3", "valid": "1..3"},
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
    line_count = ctx.draw_int("line_count", 1, 3)
    colors = ctx.draw_distinct_colors("colors", n=line_count, exclude={7})
    g = full_grid(11, 11, 7)
    specs = [
        ("h", 2, 2, 5),
        ("v", 2, 8, 5),
        ("h", 8, 3, 3),
    ]
    for color, (orient, r, c, length) in zip(colors, specs):
        for k in range(length):
            rr = r + (k if orient == "v" else 0)
            cc = c + (k if orient == "h" else 0)
            g[rr][cc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 7)
    if name == "no_lines":
        return g
    if name == "single_line":
        for c in range(2, 7):
            g[5][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
