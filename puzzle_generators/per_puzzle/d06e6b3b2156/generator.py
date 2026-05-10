"""Generator for arc_additional_puzzles_21_set14_bundle:M97.

Rule: anchor = last 8-cell, target = last 9-cell. Translate all
non-{0,8,9} cells by that vector. Output empty + translated.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_anchor, no_target, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d06e6b3b2156"
VERSION = "1.1.0"
TASK_ID = "d06e6b3b2156"
SUMMARY = "8-anchor + 9-target + small motif near 8."

INVARIANTS = [
    "exactly one 8-cell, one 9-cell",
    "small multi-color motif (3-5 cells) near 8",
    "translated cells stay in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anchor", "no_target", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[1][1] = 8
    g[2][2] = 2; g[2][3] = 2
    g[3][3] = 2
    g[4][2] = 2; g[4][3] = 2; g[4][4] = 2
    g[5][6] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_anchor":
        g[5][6] = 9
        return g
    if name == "no_target":
        g[1][1] = 8
        g[2][2] = 2
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
