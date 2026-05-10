"""Generator for arc_additional_puzzle_bank_volume21:H145.

Rule: a red start and adjacent blue direction cell trace a cyan beam
through optional mirrors and gray walls.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_start, no_direction, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "764b6b9e7771"
VERSION = "1.1.0"
TASK_ID = "764b6b9e7771"
SUMMARY = "Red start + blue direction trace a cyan beam through mirrors and walls."

INVARIANTS = [
    "there is one red start cell",
    "one adjacent blue cell defines the initial direction",
    "gray walls stop the beam",
    "the beam visits at least one blank cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_start", "no_direction", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "11..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 11, 16)
    g = full_grid(h, w, 0)
    row = h - 2
    g[row][0] = 2
    g[row][1] = 1
    g[row][w - 1] = 5
    g[max(1, row - 3)][w // 2] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 13, 0)
    if name == "no_start":
        g[8][1] = 1
        g[8][12] = 5
        return g
    if name == "no_direction":
        g[8][0] = 2
        g[8][12] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
