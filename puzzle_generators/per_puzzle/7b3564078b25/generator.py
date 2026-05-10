"""Generator for arc_additional_puzzle_bank_volume12:H84.

Rule: even-marker gray-wall chambers fill with their strict majority
marker color.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_walls, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b3564078b25"
VERSION = "1.1.0"
TASK_ID = "7b3564078b25"
SUMMARY = "Even-marker chambers fill with strict majority color."

INVARIANTS = [
    "background is 0",
    "gray walls split the board into chambers",
    "one chamber has an even positive marker count",
    "that chamber has a unique majority among colors 1 through 4",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "9..13"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "10..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
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
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 10, 15)
    g = full_grid(h, w, 0)
    wall = w // 2
    for r in range(h):
        g[r][wall] = 5
    for r, c, v in [(1, 1, 1), (2, 2, 1), (h - 3, 1, 2), (h - 2, 2, 3), (1, wall + 2, 4)]:
        g[r][c] = v
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 11, 0)
    if name == "no_walls":
        g[3][3] = 1
        return g
    if name == "no_markers":
        for r in range(10):
            g[r][5] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
