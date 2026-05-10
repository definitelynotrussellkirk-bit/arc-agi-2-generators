"""Generator for arc_puzzle_bank_sixteenth21:E110.

Rule: sparse off-diagonal cells are copied across the main diagonal.

Combinatorial axes (8): grid_h/w, size, cells, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias.
Degenerates: empty_grid, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ae0d46c67401"
VERSION = "1.1.0"
TASK_ID = "ae0d46c67401"

SUMMARY = "Sparse off-diagonal cells copied across the main diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "source cells are placed above the main diagonal",
    "transposed target cells are initially empty",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_grid", "single_cell", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "5..9"},
    "grid_w":         {"type": "int", "default": "rng 5..9", "valid": "5..9"},
    "size":           {"type": "int", "default": "rng 5..9", "valid": "5..9"},
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
        n = ctx.draw_int("size", 5, 6)
    elif difficulty == "hard":
        n = ctx.draw_int("size", 8, 9)
    else:
        n = ctx.draw_int("size", 5, 9)
    target = ctx.draw_int("cells", 3, 7)
    g = full_grid(n, n, 0)
    candidates = [(r, c) for r in range(n) for c in range(r + 1, n)]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "empty_grid":
        return g
    if name == "single_cell":
        g[2][4] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
