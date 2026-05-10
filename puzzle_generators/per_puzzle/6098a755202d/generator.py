"""Generator for arc_additional_puzzles_21_set19_bundle:M130.

Rule: 5-frame surrounds interior. For each empty cell, find nearest seed
(Manhattan); if unique → seed color; tied → 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seeds, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "6098a755202d"
VERSION = "1.1.0"
TASK_ID = "6098a755202d"
SUMMARY = "5-frame around interior with 2-3 distinct-color single-cell seeds."

INVARIANTS = [
    "exactly one closed 5-frame on outer border",
    "interior has 2-3 single-cell seeds of distinct non-{0,5} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seeds", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "interior_seeds",
                       "valid": "interior_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "framed", "valid": "framed"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    draw_frame(g, 1, 1, h - 2, w - 2, 5)
    palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
    n = rng.randint(2, 3)
    placed = 0
    while placed < n:
        sr = rng.randint(2, h - 3)
        sc = rng.randint(2, w - 3)
        if g[sr][sc] == 0:
            g[sr][sc] = palette[placed]; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # seeds without 5-frame → no boundary, voronoi extends to grid edges
        g[3][3] = 4; g[5][7] = 6
        return g
    if name == "no_seeds":
        # frame but no seeds → nothing to compute distances from
        draw_frame(g, 1, 1, h - 2, w - 2, 5)
        return g
    if name == "single_seed":
        # one seed → entire interior is its color, no ties possible
        draw_frame(g, 1, 1, h - 2, w - 2, 5)
        g[3][5] = 4
        return g
    return g
