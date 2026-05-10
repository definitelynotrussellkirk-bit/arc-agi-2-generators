"""Generator for arc_puzzle_bank_21_set14_bundle:easy_n03.

Rule: the canonical output is the exact transpose of the input grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, square_symmetric, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e3c21120e3d1"
VERSION = "1.1.0"
TASK_ID = "e3c21120e3d1"
SUMMARY = "Sparse non-square colored grids for whole-grid transposition."

INVARIANTS = [
    "background is 0",
    "grid is usually non-square",
    "nonzero cells are sparse and multicolor",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "square_symmetric", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "3..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_count":     {"type": "int", "default": "rng 5..10", "valid": "1..30"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
        cell_count = ctx.draw_int("cell_count", 4, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        cell_count = ctx.draw_int("cell_count", 8, 10)
    else:
        h = ctx.draw_int("grid_h", 4, 7)
        w = ctx.draw_int("grid_w", 7, 11)
        cell_count = ctx.draw_int("cell_count", 5, min(10, h * w))
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    for i, (r, c) in enumerate(positions[:cell_count]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    if name == "empty_grid":
        # no cells → transpose is trivially the same empty grid
        return full_grid(5, 8, 0)
    if name == "square_symmetric":
        # square grid with main-diagonal symmetry → transpose is identity
        g = full_grid(5, 5, 0)
        for r, c in [(0, 1), (1, 0), (1, 3), (3, 1), (2, 2), (3, 4), (4, 3)]:
            g[r][c] = 4
        return g
    if name == "single_cell":
        # 1×1 grid → transpose is identity, rule has no observable effect
        return [[7]]
    return full_grid(5, 8, 0)
