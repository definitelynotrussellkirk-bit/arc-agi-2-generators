"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p06 — dominoes grow into 2x2 squares.

Rule: each separated horizontal or vertical same-color domino grows
into a 2x2 square in its color (horizontal extends downward, vertical
extends rightward).

Combinatorial axes (8): grid_h, grid_w, palette_kind, domino_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, single_cell, growth_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1d9a320d33c0"
VERSION = "1.1.0"
TASK_ID = "1d9a320d33c0"
SUMMARY = "Separated horizontal and vertical dominoes grow into 2x2 squares."

INVARIANTS = [
    "background is 0",
    "each object is exactly one same-color domino",
    "horizontal dominoes have clear cells below; vertical dominoes have clear cells to the right",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "single_cell", "growth_blocked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "domino_count":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= domino_count", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_axis_dominoes",
                       "valid": "scattered_axis_dominoes"},
    "n_distinct_colors": {"type": "int", "default": "= domino_count", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_patch(grid, cells):
    h = len(grid)
    w = len(grid[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if grid[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        domino_count = ctx.draw_int("domino_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 16)
        domino_count = ctx.draw_int("domino_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        domino_count = ctx.draw_int("domino_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], domino_count)
    candidates = []
    for r in range(h - 1):
        for c in range(w - 1):
            candidates.append(("h", r, c))
            candidates.append(("v", r, c))
    rng.shuffle(candidates)
    placed = 0
    for orient, r, c in candidates:
        if placed >= domino_count:
            break
        cells = [(r, c), (r, c + 1)] if orient == "h" else [(r, c), (r + 1, c)]
        if not _clear_patch(grid, cells):
            continue
        color = colors[placed]
        for rr, cc in cells:
            grid[rr][cc] = color
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # Empty grid — rule has no domino to grow.
        return g
    if name == "single_cell":
        # Singletons (length 1) — too short to be a domino.
        g[2][2] = 4; g[5][7] = 6; g[7][3] = 7
        return g
    if name == "growth_blocked":
        # Dominoes correctly placed, but the growth target cells are
        # already occupied by another color — the rule's 2x2 expansion
        # cannot complete cleanly.
        g[2][2] = 4; g[2][3] = 4
        g[3][2] = 7; g[3][3] = 7
        return g
    return g
