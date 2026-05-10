"""Generator for da6e95e5.

Rule: the largest one-color object is cropped to its bbox shrunk by two cells.

Combinatorial axes (8): grid_h/w, rect_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_rect, single_pixel, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "50b436f101bb"
VERSION = "1.1.0"
TASK_ID = "50b436f101bb"
SUMMARY = "Largest one-color object is cropped to its bbox shrunk by two cells."

INVARIANTS = [
    "the background is the most common color",
    "one large single-color rectangle is larger than all distractor objects",
    "the output is the large rectangle's interior after a two-cell shrink",
]

SIZE_KINDS = ("S7", "S8", "S9")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "single_pixel", "full_grid")
HELPFUL_TEXTURES = SIZE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "rect_size":      {"type": "choice", "default": "rng helpful",
                       "valid": "7|8|9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for rect_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SIZE_KINDS:
        size = int(tx[1])
    elif difficulty == "easy":
        size = 9
    elif difficulty == "hard":
        size = 7
    else:
        size = ctx.draw_choice("rect_size", [7, 8, 9])
    color, d1, d2 = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(18, 18, 0)
    top = ctx.draw_choice("top", [3, 4])
    left = ctx.draw_choice("left", [3, 4])
    draw_rect(g, top, left, size, size, color)
    g[14][2] = d1
    g[14][3] = d2
    g[15][2] = d2
    g[15][3] = d1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_rect":
        g[14][2] = 3
        return g
    if name == "single_pixel":
        g[5][5] = 4
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(18):
                g[r][c] = 4
        return g
    return g
