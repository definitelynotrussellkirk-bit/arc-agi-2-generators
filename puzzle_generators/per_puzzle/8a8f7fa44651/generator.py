"""Generator for arc_puzzle_bank_21_set22_bundle:easy_p05 — diagonal dominoes extend at open ends.

Rule: each separated same-color diagonal domino extends one cell at
its open ends.

Combinatorial axes (8): grid_h, grid_w, palette_kind, domino_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, axis_aligned, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a8f7fa44651"
VERSION = "1.1.0"
TASK_ID = "8a8f7fa44651"
SUMMARY = "Separated same-color diagonal dominoes extend one cell at open ends."

INVARIANTS = [
    "background is 0",
    "each object is exactly one diagonal same-color domino",
    "dominoes are separated so extensions do not collide",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "axis_aligned", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "domino_count":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= domino_count", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_dominoes",
                       "valid": "scattered_diagonal_dominoes"},
    "n_distinct_colors": {"type": "int", "default": "= domino_count", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_wide(grid, cells):
    h = len(grid)
    w = len(grid[0])
    for r, c in cells:
        for rr in range(max(0, r - 2), min(h, r + 3)):
            for cc in range(max(0, c - 2), min(w, c + 3)):
                if grid[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        domino_count = ctx.draw_int("domino_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
        domino_count = ctx.draw_int("domino_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        domino_count = ctx.draw_int("domino_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    candidates = []
    for r in range(h):
        for c in range(w):
            for dr, dc in ((1, 1), (1, -1)):
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < h and 0 <= c2 < w:
                    candidates.append(((r, c), (r2, c2)))
    rng.shuffle(candidates)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], domino_count)
    placed = 0
    for cells in candidates:
        if placed >= domino_count:
            break
        if not _clear_wide(grid, cells):
            continue
        color = colors[placed]
        for r, c in cells:
            grid[r][c] = color
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # Empty grid — no diagonal domino to extend.
        return g
    if name == "axis_aligned":
        # Same-color cells but they're horizontally/vertically adjacent,
        # not diagonal — rule's diagonal-domino filter never matches.
        g[2][2] = 4; g[2][3] = 4
        g[5][7] = 6; g[6][7] = 6
        return g
    if name == "single_cell":
        # Singletons only — no domino, just isolated cells.
        g[2][2] = 4; g[5][5] = 6; g[7][7] = 7
        return g
    return g
