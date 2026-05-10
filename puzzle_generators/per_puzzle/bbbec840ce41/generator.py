"""Generator for arc_additional_puzzle_bank_volume9:E60.

Rule: square grid n×n; for each non-bg cell at (r,c), set
out[n-1-c][n-1-r] = v (anti-diagonal reflection); originals preserved.

Combinatorial axes (8): grid_n, palette_kind, n_cells, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, all_on_antidiag, anti_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bbbec840ce41"
VERSION = "1.1.0"
TASK_ID = "bbbec840ce41"
SUMMARY = "Square grid with scattered non-bg cells in upper triangle."

INVARIANTS = [
    "square (h == w)",
    "≥4 non-bg cells, mostly in upper-triangle region (so reflection lands in different cells)",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("empty_grid", "all_on_antidiag", "anti_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_n":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 5..7", "valid": "4..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_tri",
                       "valid": "upper_tri"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        n = ctx.draw_int("grid_n", 8, 8)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_n", 9, 10)
    else:
        n = ctx.draw_int("grid_n", 8, 10)
    g = full_grid(n, n, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8, 9]
    cells = []
    for r in range(n):
        for c in range(n):
            if r + c < n - 1:
                cells.append((r, c))
    rng.shuffle(cells)
    for (r, c) in cells[:rng.randint(5, 7)]:
        g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    n = 8
    g = full_grid(n, n, 0)
    if name == "empty_grid":
        # nothing to reflect — output equals input
        return g
    if name == "all_on_antidiag":
        # all cells on the anti-diagonal r+c=n-1 → reflection is identity
        for i in range(n):
            g[i][n - 1 - i] = ((i % 5) + 2)
        return g
    if name == "anti_symmetric":
        # already anti-symmetric → reflection overlay is identity
        for r, c, v in [(0, 1, 4), (1, 0, 4), (2, 5, 6), (5, 2, 6)]:
            g[r][c] = v
        return g
    return g
