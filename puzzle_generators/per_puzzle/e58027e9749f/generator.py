"""Generator for arc_puzzle_bank_21_set19_bundle:easy_p03.

Rule: sparse cells above the main diagonal of a square grid are echoed
across the diagonal (transposed positions).

Combinatorial axes (8): grid_size, palette_kind, cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_symmetric, on_diagonal, empty_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e58027e9749f"
VERSION = "1.1.0"
TASK_ID = "e58027e9749f"
SUMMARY = "Sparse cells in a square grid are echoed across the main diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "nonzero source cells are placed away from occupied reflected targets",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("already_symmetric", "on_diagonal", "empty_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "size":           {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_count":     {"type": "int", "default": "rng 3..6", "valid": "1..16"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "above_diagonal",
                       "valid": "above_diagonal"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..6",
                          "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
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

    candidates = [(r, c) for r in range(size) for c in range(r + 1, size)]
    rng.shuffle(candidates)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for r, c in candidates[: min(cell_count, len(candidates))]:
        grid[r][c] = rng.choice(colors)
    return grid


def _draw_from_degenerate(name, rng):
    size = 7
    g = full_grid(size, size, 0)
    if name == "already_symmetric":
        # input has both halves filled — rule output equals input
        for r, c in [(0, 2), (1, 4), (2, 5)]:
            g[r][c] = 5
            g[c][r] = 5
        return g
    if name == "on_diagonal":
        # cells ON main diagonal — mirror to themselves
        for i in [1, 3, 5]:
            g[i][i] = 4
        return g
    if name == "empty_grid":
        return g
    return g
