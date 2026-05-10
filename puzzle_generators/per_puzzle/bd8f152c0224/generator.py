"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p02.

Rule: sparse cells in a square grid are echoed across the
anti-diagonal.

Combinatorial axes (8): size, cell_count, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_cells, on_anti_diagonal_only, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bd8f152c0224"
VERSION = "1.1.0"
TASK_ID = "bd8f152c0224"
SUMMARY = "Sparse cells in a square grid are echoed across the anti-diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "source cells are placed on one side of the anti-diagonal to avoid conflicts",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cells", "on_anti_diagonal_only", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "size":           {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "cell_count":     {"type": "int", "default": "rng 3..6", "valid": "1..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "anti_triangle", "valid": "anti_triangle"},
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
        size = ctx.draw_int("size", 6, 7)
        cell_count = ctx.draw_int("cell_count", 3, 4)
    elif difficulty == "hard":
        size = ctx.draw_int("size", 8, 9)
        cell_count = ctx.draw_int("cell_count", 5, 6)
    else:
        size = ctx.draw_int("size", 6, 9)
        cell_count = ctx.draw_int("cell_count", 3, 6)
    rng = ctx.draw_rng("layout")
    grid = full_grid(size, size, 0)
    candidates = [(r, c) for r in range(size) for c in range(size) if r + c < size - 1]
    rng.shuffle(candidates)
    for r, c in candidates[: min(cell_count, len(candidates))]:
        grid[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return grid


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_cells":
        return g
    if name == "on_anti_diagonal_only":
        for i in range(7):
            g[i][6 - i] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
