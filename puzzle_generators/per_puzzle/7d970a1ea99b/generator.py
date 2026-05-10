"""Generator for arc_puzzle_bank_eighth_21_bundle:easy_54_reflect_main_diagonal.

Rule: sparse square grid whose nonzero cells are reflected across the
main diagonal.

Combinatorial axes (8): side, palette_kind, n_cells, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, on_diagonal_only, already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7d970a1ea99b"
VERSION = "1.1.0"
TASK_ID = "7d970a1ea99b"
SUMMARY = "Sparse square grid whose nonzero cells are reflected across the main diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "at least one nonzero cell lies off the main diagonal",
    "source cells do not already make a fully symmetric pattern",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "on_diagonal_only", "already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "side":           {"type": "int", "default": "rng 6..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 3..7", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "off_diagonal", "valid": "off_diagonal"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        n = ctx.draw_int("side", 6, 7)
        n_cells = ctx.draw_int("n_cells", 2, 4)
    elif difficulty == "hard":
        n = ctx.draw_int("side", 9, 10)
        n_cells = ctx.draw_int("n_cells", 5, 7)
    else:
        n = ctx.draw_int("side", 6, 10)
        n_cells = ctx.draw_int("n_cells", 3, 7)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    rng = ctx.draw_rng("cells")
    g = full_grid(n, n, 0)
    candidates = [(r, c) for r in range(n) for c in range(n) if r != c]
    rng.shuffle(candidates)
    for i, (r, c) in enumerate(candidates[:n_cells]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    n = 7
    g = full_grid(n, n, 0)
    if name == "empty_grid":
        # nothing to reflect — output equals input
        return g
    if name == "on_diagonal_only":
        # all cells sit on the main diagonal → reflection is identity
        for i in range(n):
            g[i][i] = ((i % 7) + 1)
        return g
    if name == "already_symmetric":
        # input is already mirror-symmetric across the main diagonal → rule no-op
        for r, c in [(1, 3), (3, 1), (2, 5), (5, 2)]:
            g[r][c] = 4
        return g
    return g
