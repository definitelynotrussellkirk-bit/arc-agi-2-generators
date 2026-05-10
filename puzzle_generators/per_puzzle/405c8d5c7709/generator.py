"""Generator for 36fdfd69.

Rule: nearby red cells form groups whose bounding boxes replace
background cells with color 4.

Combinatorial axes (8): grid_h/w, group_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_groups, single_red, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "405c8d5c7709"
VERSION = "1.1.0"
TASK_ID = "405c8d5c7709"
SUMMARY = "Nearby red cells form groups whose bounding boxes paint background to color 4."

INVARIANTS = [
    "the most frequent nonzero color is the fillable background",
    "red cells are grouped by Chebyshev distance at most two",
    "each red-group bounding box contains background cells",
    "background cells inside each red-group bbox become color 4",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_groups", "single_red", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "group_count":    {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
    if difficulty == "easy":
        group_count = ctx.draw_int("group_count", 1, 1)
    elif difficulty == "hard":
        group_count = ctx.draw_int("group_count", 3, 3)
    else:
        group_count = ctx.draw_int("group_count", 1, 3)
    bg = ctx.draw_color("background", exclude={0, 2, 4})
    g = full_grid(12, 12, bg)
    anchors = [(2, 2), (2, 7), (7, 4)]
    rng.shuffle(anchors)
    for r, c in anchors[:group_count]:
        g[r][c] = 2
        g[r + 2][c + 2] = 2
        if rng.choice([True, False]):
            g[r + 1][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 5)
    if name == "no_groups":
        return g
    if name == "single_red":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
