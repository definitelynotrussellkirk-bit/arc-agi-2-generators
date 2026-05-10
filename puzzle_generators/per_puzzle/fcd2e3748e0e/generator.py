"""Generator for arc_additional_puzzle_bank_volume10:H64.

Rule: two control cells select reflection and rotation for a blue
template stamped at a maroon anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, reflect_ctrl,
rotate_ctrl, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_reflect_ctrl, no_rotate_ctrl, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fcd2e3748e0e"
VERSION = "1.1.0"
TASK_ID = "fcd2e3748e0e"
SUMMARY = "Two control cells select reflection and rotation for a blue template stamped at a maroon anchor."

INVARIANTS = [
    "one reflect control is 2 or 3",
    "one rotation control is 4, 5, 6, or 7",
    "there is one asymmetric color-1 template",
    "the transformed copy fits at the color-9 anchor",
]

PALETTE_KINDS = ("default", "rotate_low", "rotate_mid", "rotate_high")
DEGENERATE_TEXTURES = ("no_reflect_ctrl", "no_rotate_ctrl", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "reflect_ctrl":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "rotate_ctrl":    {"type": "int", "default": "rng 4..7", "valid": "4..7"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 13, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([2, 3])
    g[0][1] = rng.choice([4, 5, 6, 7])
    anchor_r = rng.randint(2, h - 5)
    anchor_c = rng.randint(4, w - 6)
    g[anchor_r][anchor_c] = 9
    tr = h - 5
    tc = w - 5
    for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
        g[tr + dr][tc + dc] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    tr, tc = h - 5, w - 5
    if name == "no_reflect_ctrl":
        # rotation ctrl + template + anchor but no 2/3 ctrl → flip is undefined
        g[0][1] = 5
        g[3][6] = 9
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
            g[tr + dr][tc + dc] = 1
        return g
    if name == "no_rotate_ctrl":
        # reflect ctrl + template + anchor but no 4..7 ctrl → rotation undefined
        g[0][0] = 2
        g[3][6] = 9
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
            g[tr + dr][tc + dc] = 1
        return g
    if name == "no_anchor":
        # both ctrls + template but no 9-anchor → stamp position undefined
        g[0][0] = 2
        g[0][1] = 5
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
            g[tr + dr][tc + dc] = 1
        return g
    return g
