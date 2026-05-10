"""Generator for arc_additional_puzzle_bank_volume3:H20.

Rule: pivot = first 2-cell. For each 1-cell, rotate around pivot by
4 quarter-turns and paint at all rotation positions in bounds.

Combinatorial axes (8): grid_n, palette_kind, n_ones,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot, no_ones, ones_outside_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ba0c6a5828f9"
VERSION = "1.1.0"
TASK_ID = "ba0c6a5828f9"
SUMMARY = "Square grid with 2-pivot in center + 1-cells in upper-left."

INVARIANTS = [
    "grid is square (so 4-fold rotation fits)",
    "exactly one 2-cell (pivot) in center",
    "1-2 1-cells near pivot, all rotation images stay in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_ones", "ones_outside_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_n":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ones":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "pivot_center",
                       "valid": "pivot_center"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        n = ctx.draw_int("grid_n", 7, 7)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_n", 8, 9)
    else:
        n = ctx.draw_int("grid_n", 7, 9)
    h = w = n
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pr = h // 2; pc = w // 2
    g[pr][pc] = 2
    candidates = []
    for r in range(max(0, pr - 2), pr):
        for c in range(max(0, pc - 2), pc + 1):
            if (r, c) != (pr, pc):
                candidates.append((r, c))
    rng.shuffle(candidates)
    n_ones = rng.randint(2, 3)
    for r, c in candidates[:n_ones]:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    n = 8
    g = full_grid(n, n, 0)
    if name == "no_pivot":
        # no 2-cell → rotation center is undefined, rule has nothing to rotate around
        g[2][2] = 1
        g[2][3] = 1
        return g
    pr = n // 2; pc = n // 2
    g[pr][pc] = 2
    if name == "no_ones":
        # pivot exists but no 1-cells → nothing to rotate
        return g
    if name == "ones_outside_grid":
        # 1-cell placed where one of its rotation images is out-of-bounds
        g[0][0] = 1
        return g
    return g
