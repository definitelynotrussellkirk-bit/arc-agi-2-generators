"""Generator for f8be4b64.

Rule: green-armed pluses cast row and column rays of their center colors,
with column priority.

Combinatorial axes (8): grid_h/w, plus_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_pluses, no_arms, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3dbd1a94c4d7"
VERSION = "1.1.0"
TASK_ID = "3dbd1a94c4d7"
SUMMARY = "Green-armed pluses cast row/col rays of center colors with column priority."

INVARIANTS = [
    "each plus has four color-3 arms",
    "the plus center color supplies the ray color",
    "rays stop at other plus arms",
    "column projections take priority over row projections where both apply",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pluses", "no_arms", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "plus_count":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
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


def _plus(g, r, c, color):
    g[r][c] = color
    g[r - 1][c] = 3
    g[r + 1][c] = 3
    g[r][c - 1] = 3
    g[r][c + 1] = 3


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        plus_count = ctx.draw_int("plus_count", 1, 1)
    elif difficulty == "hard":
        plus_count = ctx.draw_int("plus_count", 3, 3)
    else:
        plus_count = ctx.draw_int("plus_count", 1, 3)
    colors = ctx.draw_distinct_colors("center_colors", n=plus_count, exclude={0, 3})
    g = full_grid(13, 13, 0)
    centers = [(3, 3), (9, 5), (5, 10)]
    for color, center in zip(colors, centers):
        _plus(g, center[0], center[1], color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_pluses":
        return g
    if name == "no_arms":
        g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
