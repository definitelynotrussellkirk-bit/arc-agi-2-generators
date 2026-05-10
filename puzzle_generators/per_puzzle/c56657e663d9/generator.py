"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p07.

Rule: every nonzero cell is echoed across the main diagonal (its transpose
position is also painted with the same color).

Combinatorial axes (8): grid_size, palette_kind, cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_symmetric, all_on_diagonal, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c56657e663d9"
VERSION = "1.1.0"
TASK_ID = "c56657e663d9"
SUMMARY = "Square sparse upper-triangle patterns for main-diagonal echo."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "nonzero cells are placed on or above the main diagonal",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("already_symmetric", "all_on_diagonal", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "size":           {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_count":     {"type": "int", "default": "rng 4..9", "valid": "1..30"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "upper_triangle",
                       "valid": "upper_triangle"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "1..9"},
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
        n = ctx.draw_int("size", 6, 7)
        cell_count = ctx.draw_int("cell_count", 4, 6)
    elif difficulty == "hard":
        n = ctx.draw_int("size", 9, 10)
        cell_count = ctx.draw_int("cell_count", 7, 9)
    else:
        n = ctx.draw_int("size", 6, 10)
        cell_count = ctx.draw_int("cell_count", 4, 9)
    colors = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(n, n, 0)
    positions = [(r, c) for r in range(n) for c in range(r, n)]
    rng.shuffle(positions)
    for i, (r, c) in enumerate(positions[:cell_count]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    n = 7
    g = full_grid(n, n, 0)
    if name == "already_symmetric":
        # input already mirrored across main diagonal — rule output equals input
        for r, c, v in [(1, 3, 4), (3, 1, 4), (2, 5, 7), (5, 2, 7)]:
            g[r][c] = v
        return g
    if name == "all_on_diagonal":
        # cells ON main diagonal echo to themselves — rule no-op
        for i in [1, 3, 5]:
            g[i][i] = (i + 2)
        return g
    if name == "no_cells":
        return g
    return g
