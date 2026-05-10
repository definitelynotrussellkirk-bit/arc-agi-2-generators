"""Generator for arc_puzzle_bank_next_21_bundle:easy_12_diagonal_shadow_down_right.

Rule: each color-3 cell with a zero down-right neighbor casts a 5 there.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, all_at_corner, shadow_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e443791433ff"
VERSION = "1.1.0"
TASK_ID = "e443791433ff"
SUMMARY = "Sparse 3-cells with open down-right shadows that the rule paints as 5."

INVARIANTS = [
    "background is 0",
    "source cells are color 3",
    "at least one color-3 cell has a zero down-right neighbor",
    "source cells avoid the lower and right borders when intended to cast",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "all_at_corner", "shadow_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 3..7", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior_with_shadow_room",
                       "valid": "interior_with_shadow_room"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_seeds = ctx.draw_int("n_seeds", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
        n_seeds = ctx.draw_int("n_seeds", 3, 7)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)

    cells = [(r, c) for r in range(h - 1) for c in range(w - 1)]
    rng.shuffle(cells)
    placed = 0
    for r, c in cells:
        if placed >= n_seeds:
            break
        if g[r][c] == 0 and g[r + 1][c + 1] == 0:
            g[r][c] = 3
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank or unrelated colors → no source cells, rule effect is empty
        g[3][3] = 6; g[5][5] = 8
        return g
    if name == "all_at_corner":
        # all 3-seeds on the bottom row or right column → no down-right neighbor exists
        g[h - 1][2] = 3; g[h - 1][5] = 3
        g[2][w - 1] = 3; g[5][w - 1] = 3
        return g
    if name == "shadow_already_filled":
        # seed has down-right neighbor, but it's already non-zero → rule predicate fails
        g[2][2] = 3; g[3][3] = 7
        g[5][4] = 3; g[6][5] = 7
        return g
    return g
