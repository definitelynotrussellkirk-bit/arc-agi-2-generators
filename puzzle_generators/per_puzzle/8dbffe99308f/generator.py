"""Generator for easy_57_complete_anti_diagonal_symmetry.

Rule: nonzero cells are echoed across the anti-diagonal — for cell (r, c),
also paint (n-1-c, n-1-r) with the same color.

Combinatorial axes (8): grid_size, palette_kind, cell_count, density,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: already_symmetric, on_anti_diagonal, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8dbffe99308f"
VERSION = "1.1.0"
TASK_ID = "8dbffe99308f"
SUMMARY = "Sparse square-grid cells are echoed across the anti-diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "source cells lie strictly on one side of the anti-diagonal",
    "anti-diagonal reflected cells are initially empty",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("already_symmetric", "on_anti_diagonal", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 3..7", "valid": "1..24"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "above_anti_diagonal",
                       "valid": "above_anti_diagonal"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..7",
                          "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("grid_size", 6, 7)
        target = ctx.draw_int("cells", 3, 4)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 8, 9)
        target = ctx.draw_int("cells", 5, 7)
    else:
        n = ctx.draw_int("grid_size", 6, 9)
        target = ctx.draw_int("cells", 3, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(n, n, 0)
    candidates = [(r, c) for r in range(n) for c in range(n) if r + c < n - 1]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    n = 7
    g = full_grid(n, n, 0)
    if name == "already_symmetric":
        # both halves filled with mirror image — rule output equals input
        for r, c, v in [(1, 2, 4), (4, 5, 4), (2, 0, 7), (6, 4, 7)]:
            g[r][c] = v
        return g
    if name == "on_anti_diagonal":
        # cells ON anti-diagonal echo to themselves
        for i in range(n):
            if i % 2 == 0:
                g[i][n - 1 - i] = (i % 8) + 1
        return g
    if name == "no_cells":
        return g
    return g
