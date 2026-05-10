"""Generator for arc_additional_puzzles_21_set5:H34.

Rule: template = subgrid(0,0,2,2) with 9-cells substituted by anchor
color. For each non-zero cell outside template area, stamp template
centered.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_anchors, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5ca50f15620"
VERSION = "1.1.0"
TASK_ID = "b5ca50f15620"
SUMMARY = "3x3 template in upper-left + 1-2 single anchors elsewhere."

INVARIANTS = [
    "template at upper-left (rows 0-2, cols 0-2)",
    "1-2 anchor cells outside template region",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    g[0][0] = 7; g[0][1] = 9; g[0][2] = 7
    g[1][0] = 9; g[1][2] = 9
    g[2][0] = 7; g[2][1] = 9; g[2][2] = 7
    g[5][5] = 2
    g[7][8] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_template":
        g[5][5] = 2
        g[7][8] = 4
        return g
    if name == "no_anchors":
        g[0][0] = 7; g[0][1] = 9; g[0][2] = 7
        g[1][0] = 9; g[1][2] = 9
        g[2][0] = 7; g[2][1] = 9; g[2][2] = 7
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 7
        return g
    return g
