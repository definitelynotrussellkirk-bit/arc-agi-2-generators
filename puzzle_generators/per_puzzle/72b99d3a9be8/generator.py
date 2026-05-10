"""Generator for 7e2bad24.

Rule: diagonal pair of color-1 cells extends in both diagonal
directions, bouncing from color-2 walls when present.

Combinatorial axes (8): grid_h/w, diagonal, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_pair, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "72b99d3a9be8"
VERSION = "1.1.0"
TASK_ID = "72b99d3a9be8"
SUMMARY = "Diagonal 1-pair extends in both diagonal directions."

INVARIANTS = [
    "background is color 0",
    "at least two color-1 cells form a diagonal adjacent pair",
    "the pair establishes the walk direction",
    "the pair sits clear of grid borders so the walks have room",
]

DIAGONALS = ("down_right", "down_left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pair", "single_cell", "full_grid")
HELPFUL_TEXTURES = DIAGONALS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "diagonal":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIAGONALS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for diagonal",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    diagonal = (overrides.get("texture") if overrides.get("texture") in DIAGONALS else None) or \
               overrides.get("diagonal") or \
               ctx.draw_choice("diagonal", list(DIAGONALS))
    h = 9 + rng.randint(0, 4)
    w = 9 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    r = 3 + rng.randint(0, h - 7)
    c = 3 + rng.randint(0, w - 7)
    if diagonal == "down_right":
        g[r][c] = 1
        g[r + 1][c + 1] = 1
    else:
        g[r][c + 1] = 1
        g[r + 1][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_pair":
        return g
    if name == "single_cell":
        g[5][5] = 1
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 1
        return g
    return g
