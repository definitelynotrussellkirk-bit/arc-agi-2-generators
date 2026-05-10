"""Generator for 11b:m75 — quadrant majority summary.

Rule: divide grid into 2x2 quadrants. For each quadrant, output the
most common non-zero color in that quadrant. Output is 2x2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, half_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, single_quadrant_filled, tied_majority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b25434a1b56e"
VERSION = "1.1.0"
TASK_ID = "b25434a1b56e"
SUMMARY = "4 quadrants each with 1 dominant scattered color."

INVARIANTS = [
    "background is 0",
    "grid h, w are even (so 4 quadrants are equal-sized)",
    "each quadrant has scattered cells with one dominant color (≥3 cells)",
    "all 4 quadrants use distinct dominant colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "single_quadrant_filled", "tied_majority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "half_h":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "half_w":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "four_quadrants_majority",
                       "valid": "four_quadrants_majority"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
        hh = ctx.draw_int("half_h", 3, 3)
        hw = ctx.draw_int("half_w", 3, 3)
    elif difficulty == "hard":
        hh = ctx.draw_int("half_h", 4, 5)
        hw = ctx.draw_int("half_w", 4, 5)
    else:
        hh = ctx.draw_int("half_h", 3, 5)
        hw = ctx.draw_int("half_w", 3, 5)
    h = hh * 2; w = hw * 2
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    quads = [(0, 0, hh, hw), (0, hw, hh, w), (hh, 0, h, hw), (hh, hw, h, w)]
    for (r1, c1, r2, c2), color in zip(quads, palette):
        cells = [(r, c) for r in range(r1, r2) for c in range(c1, c2)]
        n = rng.randint(3, max(3, len(cells) // 2))
        for r, c in rng.sample(cells, min(n, len(cells))):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    hh, hw = 3, 4
    h, w = hh * 2, hw * 2
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # blank → no quadrant has a majority color
        return g
    if name == "single_quadrant_filled":
        # only one quadrant filled → other 3 quadrants have no majority
        for r in range(hh):
            for c in range(hw): g[r][c] = 4
        return g
    if name == "tied_majority":
        # quadrant has two colors with equal count → no strict majority
        g[0][0] = 4; g[0][1] = 6
        g[1][0] = 4; g[1][1] = 6   # tied 2-2 in this quadrant
        for r in range(hh):
            for c in range(hw): g[r][hw + c] = 7
        for r in range(hh):
            for c in range(hw): g[hh + r][c] = 8
        for r in range(hh):
            for c in range(hw): g[hh + r][hw + c] = 9
        return g
    return g
