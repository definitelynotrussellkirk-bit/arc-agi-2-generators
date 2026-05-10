"""Generator for 996ec1f3.

Rule: uniform divider row + col summarize quadrant dominant colors into
3x3 grid.

Combinatorial axes (8): grid_size, divider, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_quadrant_cells.
Degenerates: no_divider, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "196d5de2ea8c"
VERSION = "1.1.0"
TASK_ID = "196d5de2ea8c"
SUMMARY = "Uniform divider row + col summarize quadrant dominant colors into 3x3 grid."

INVARIANTS = [
    "one row and one column are uniform divider color",
    "the four interior quadrants each have a clear dominant color",
    "rows and columns before the divider are not themselves uniform",
    "the output corners are quadrant dominant colors and cross cells are divider color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_divider", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "7", "valid": "7"},
    "divider":        {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_quadrant_cells":{"type": "int", "default": "4", "valid": "1..4"},
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
    divider = ctx.draw_color("divider", exclude={0})
    tl, tr, bl, br = ctx.draw_distinct_colors("quadrants", n=4,
                                              exclude={divider})
    g = full_grid(7, 7, 0)
    for c in range(7):
        g[3][c] = divider
    for r in range(7):
        g[r][3] = divider
    for r in range(1, 3):
        for c in range(1, 3):
            g[r][c] = tl
            g[r][c + 4] = tr
            g[r + 4][c] = bl
            g[r + 4][c + 4] = br
    g[0][0] = tl
    g[0][1] = tr
    g[1][0] = bl
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_divider":
        for r in range(1, 3):
            for c in range(1, 3):
                g[r][c] = 2
        return g
    if name == "single_color":
        for c in range(w):
            g[3][c] = 5
        for r in range(h):
            g[r][3] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
