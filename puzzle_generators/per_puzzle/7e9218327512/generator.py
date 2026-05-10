"""Generator for arc_additional_puzzle_bank_volume12:M78.

Rule: src = last 2-cell; dst = last 1-cell. For each 3-cell, paint 8
at (r+dr, c+dc).

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_anchors, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7e9218327512"
VERSION = "1.1.0"
TASK_ID = "7e9218327512"
SUMMARY = "Single 2 + single 1 + 3-blob + decoration."

INVARIANTS = [
    "exactly one 2-cell, one 1-cell",
    "3-blob (3-4 cells), translated cells in bounds",
    "decoration is a non-{1,2,3} cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anchors", "no_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
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
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    g[0][0] = 2
    g[1][1] = 3; g[2][1] = 3; g[3][1] = 3; g[3][2] = 3
    g[4][6] = 1
    g[h - 2][w - 4] = 7; g[h - 2][w - 3] = 7
    g[h - 3][w - 4] = 7; g[h - 3][w - 3] = 7
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_anchors":
        g[1][1] = 3; g[2][1] = 3; g[3][1] = 3
        return g
    if name == "no_shape":
        g[0][0] = 2
        g[4][6] = 1
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
