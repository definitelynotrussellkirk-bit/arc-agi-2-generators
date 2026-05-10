"""Generator for arc_puzzle_bank_21_set4:S4_H1 — 4-fold symmetry replication.

Rule: each non-zero cell is replicated to its 4 mirrored positions (LR,
UD, 180-rotation), filling 4-fold symmetry.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, cells_outside_quadrant, already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a950d6dbe2e0"
VERSION = "1.1.0"
TASK_ID = "a950d6dbe2e0"
SUMMARY = "2-4 non-zero cells in distinct colors in the upper-left quadrant of the grid."

INVARIANTS = [
    "background is 0",
    "2-4 non-zero cells in colors located in the upper-left quadrant",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "cells_outside_quadrant", "already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8 (even)", "valid": "4..14 (even)"},
    "grid_w":         {"type": "int", "default": "rng 6..8 (even)", "valid": "4..14 (even)"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_left_quadrant",
                       "valid": "upper_left_quadrant"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h_raw = ctx.draw_int("grid_h", 6, 6)
        w_raw = ctx.draw_int("grid_w", 6, 6)
    elif difficulty == "hard":
        h_raw = ctx.draw_int("grid_h", 7, 8)
        w_raw = ctx.draw_int("grid_w", 7, 8)
    else:
        h_raw = ctx.draw_int("grid_h", 6, 8)
        w_raw = ctx.draw_int("grid_w", 6, 8)
    h = h_raw + (h_raw % 2)
    w = w_raw + (w_raw % 2)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    half_r = h // 2; half_c = w // 2
    n = rng.randint(2, 4)
    for _ in range(n):
        for _t in range(40):
            r = rng.randint(0, half_r - 1); c = rng.randint(0, half_c - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid → 4-fold replication of nothing
        return g
    if name == "cells_outside_quadrant":
        # source cells in lower/right quadrants → invariant violated, replication overlaps
        g[4][1] = 4  # lower-left
        g[1][4] = 6  # upper-right
        return g
    if name == "already_symmetric":
        # input already 4-fold symmetric → rule is identity
        for r, c in [(1, 1), (1, w - 2), (h - 2, 1), (h - 2, w - 2)]:
            g[r][c] = 4
        return g
    return g
