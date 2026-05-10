"""Generator for v2_meta_puzzles:E4.

Rule: for each color-2 cell at (r, c), if (r, c+1) is in bounds,
paint it color 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, cell_at_right_edge, neighbor_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c35533cc389"
VERSION = "1.1.0"
TASK_ID = "2c35533cc389"
SUMMARY = "Sparse color-2 cells; each must have an empty cell to its right."

INVARIANTS = [
    "background is 0",
    "2-4 color-2 cells with at least column < w-1 (room to its right)",
    "the cell immediately to the right of each color-2 is bg",
]

PALETTE_KINDS = ("default", "few", "many", "varied")
DEGENERATE_TEXTURES = ("no_cells", "cell_at_right_edge", "neighbor_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "non_right_edge",
                       "valid": "non_right_edge"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_cells", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_cells", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 6, 8)
        n = ctx.draw_int("n_cells", 2, 4)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(80):
        if placed >= n: break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 2)
        if g[r][c] != 0 or g[r][c + 1] != 0: continue
        g[r][c] = 2
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid — no 2-cells to paint right of
        return g
    if name == "cell_at_right_edge":
        # 2-cell on rightmost col → no in-bounds neighbor to paint
        g[2][w - 1] = 2
        return g
    if name == "neighbor_already_filled":
        # 2-cell with a non-zero neighbor to the right → predicate "empty right" fails
        g[1][2] = 2; g[1][3] = 4
        g[3][1] = 2; g[3][2] = 6
        return g
    return g
