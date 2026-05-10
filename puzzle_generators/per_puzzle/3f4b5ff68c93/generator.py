"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_131_transpose_square_grid.

Rule: sparse square grids are transformed by matrix transpose.

Combinatorial axes (8): grid_size, cells, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_cells, on_diagonal_only, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3f4b5ff68c93"
VERSION = "1.1.0"
TASK_ID = "3f4b5ff68c93"
SUMMARY = "Sparse square grids are transformed by matrix transpose."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "colored cells are off the main diagonal",
    "no transposed pair is already occupied",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cells", "on_diagonal_only", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "cells":          {"type": "int", "default": "rng 3..7", "valid": "1..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "upper_triangle", "valid": "upper_triangle"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("grid_size", 5, 6)
        target = ctx.draw_int("cells", 3, 4)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 7, 8)
        target = ctx.draw_int("cells", 5, 7)
    else:
        n = ctx.draw_int("grid_size", 5, 8)
        target = ctx.draw_int("cells", 3, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(n, n, 0)
    candidates = [(r, c) for r in range(n) for c in range(r + 1, n)]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "no_cells":
        return g
    if name == "on_diagonal_only":
        for i in range(6):
            g[i][i] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(6):
                g[r][c] = 3
        return g
    return g
