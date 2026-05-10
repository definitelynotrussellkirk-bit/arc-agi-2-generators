"""Generator for arc_puzzle_bank_seventh21:E44.

Rule: sparse square grids reflected across the anti-diagonal.

Combinatorial axes (8): grid_h/w, grid_size, cells, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: empty_grid, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6ccc3318a707"
VERSION = "1.1.0"
TASK_ID = "6ccc3318a707"

SUMMARY = "Sparse square grids reflected across the anti-diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "source cells lie strictly on one side of the anti-diagonal",
    "no reflected target is already occupied",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_grid", "single_cell", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "grid_size":      {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "cells":          {"type": "int", "default": "rng 3..7", "valid": "3..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n = ctx.draw_int("grid_size", 6, 7)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 8, 9)
    else:
        n = ctx.draw_int("grid_size", 6, 9)
    target = ctx.draw_int("cells", 3, 7)
    g = full_grid(n, n, 0)
    candidates = [(r, c) for r in range(n) for c in range(n) if r + c < n - 1]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "empty_grid":
        return g
    if name == "single_cell":
        g[1][2] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
