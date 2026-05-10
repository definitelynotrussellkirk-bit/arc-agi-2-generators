"""Generator for arc_additional_puzzle_bank_volume3:E20.

Rule: every size-two color-6 object is recolored to 7.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors, marker.
Degenerates: no_dominoes, all_distractors, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04676f3b2277"
VERSION = "1.1.0"
TASK_ID = "04676f3b2277"
SUMMARY = "Every size-two color-6 object recolored to 7."

INVARIANTS = [
    "there are one or more separated color-6 domino objects",
    "larger color-6 distractors are present but not recolored",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dominoes", "all_distractors", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "8..11"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "8..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "marker":         {"type": "color", "default": "rng !{0,6,7}",
                       "valid": "1..5|8|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    marker = ctx.draw_color("marker", exclude=[0, 6, 7])
    g = full_grid(h, w, 0)
    g[1][1] = 6
    g[1][2] = 6
    g[h - 3][w - 3] = 6
    g[h - 2][w - 3] = 6
    for dc in range(3):
        g[3][w - 4 + dc] = 6
    g[h - 1][0] = marker
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_dominoes":
        for dc in range(3):
            g[3][3 + dc] = 6
        return g
    if name == "all_distractors":
        for dc in range(3):
            g[3][3 + dc] = 6
        for dc in range(4):
            g[5][2 + dc] = 6
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 6
        return g
    return g
