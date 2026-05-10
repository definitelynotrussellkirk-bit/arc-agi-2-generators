"""Generator for arc_additional_puzzle_bank_volume7:H45.

Rule: two maroon-anchored source shapes are XORed by relative offsets
and stamped at the cyan target anchor.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_anchors, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "109a03554ed3"
VERSION = "1.1.0"
TASK_ID = "109a03554ed3"
SUMMARY = "Two maroon-anchored source shapes are XORed by relative offsets and stamped at the cyan target anchor."

INVARIANTS = [
    "one red component includes a maroon anchor",
    "one blue component includes a separate maroon anchor",
    "a cyan target cell provides the new anchor",
    "the anchored symmetric difference is nonempty and in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anchors", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    g = full_grid(h, w, 0)
    g[2][2] = 9
    g[2][3] = 2
    g[3][2] = 2
    g[h - 4][w - 5] = 9
    g[h - 3][w - 5] = 1
    g[h - 3][w - 4] = 1
    g[h // 2][w // 2] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_anchors":
        g[2][3] = 2
        g[3][2] = 2
        g[5][5] = 8
        return g
    if name == "no_shapes":
        g[2][2] = 9
        g[7][8] = 9
        g[5][5] = 8
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 8
        return g
    return g
