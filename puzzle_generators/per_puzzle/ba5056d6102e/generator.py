"""Generator for 13b:m89 — boolean intersection of two halves.

Rule: a horizontal 5-line splits the grid. Top half has color A cells,
bottom half color B. Output is the top-half-sized grid where cells are
8 iff both halves have non-bg in that column-position.

Combinatorial axes (8): half_h, grid_w, palette_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_intersection, identical_halves.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ba5056d6102e"
VERSION = "1.1.0"
TASK_ID = "ba5056d6102e"
SUMMARY = "Two equal-height halves separated by a horizontal 5-divider; AND of their non-bg masks."

INVARIANTS = [
    "background is 0",
    "exactly one full-width row of 5s separates the grid into two equal-height halves",
    "top half has only color-A non-bg cells; bottom half has only color-B non-bg cells",
    "the AND of their masks has at least 1 hit (so output is not all-zero)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_intersection", "identical_halves")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "half_h":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_halves_with_divider",
                       "valid": "two_halves_with_divider"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "scattered", "valid": "scattered"},
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
        half = ctx.draw_int("half_h", 4, 4)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        half = ctx.draw_int("half_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        half = ctx.draw_int("half_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    h = half * 2 + 1
    g = full_grid(h, w, 0)
    for c in range(w):
        g[half][c] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 9], 2)
    a, b = palette
    while True:
        for r in range(half):
            for c in range(w):
                if rng.random() < 0.30: g[r][c] = a
                else: g[r][c] = 0
        for r in range(half + 1, h):
            for c in range(w):
                if rng.random() < 0.30: g[r][c] = b
                else: g[r][c] = 0
        hit = False
        for c in range(w):
            for r in range(half):
                if g[r][c] != 0 and g[r + half + 1][c] != 0:
                    hit = True; break
            if hit: break
        if hit: break
    return g


def _draw_from_degenerate(name, rng):
    half = 4; w = 8; h = half * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # missing divider row → cannot identify the two halves, rule undefined
        g[1][2] = 4; g[2][5] = 4
        g[6][2] = 6; g[7][5] = 6
        return g
    if name == "no_intersection":
        # halves share no column-positions → AND mask is all-zero, output blank
        for c in range(w):
            g[half][c] = 5
        g[1][1] = 4; g[2][3] = 4  # left side
        g[6][5] = 6; g[7][7] = 6  # right side
        return g
    if name == "identical_halves":
        # halves are mirror copies → AND mask matches every non-bg position
        for c in range(w):
            g[half][c] = 5
        for (r, c) in [(1, 2), (2, 5), (3, 1)]:
            g[r][c] = 4
            g[half + 1 + (half - 1 - r)][c] = 6  # mirror
        return g
    return g
