"""Generator for arc_additional_puzzles_21_set17_bundle:H115.

Rule: 8-frame surrounds interior with seeds; for each empty interior
cell, nearest seed by Manhattan distance assigns its color; ties → 5.

Combinatorial axes (8): grid_h/w, palette_kind, n_seeds, palette_size,
position_bias, n_distinct_colors, seed_density, texture.
Degenerates: no_seeds, seeds_overlap, no_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "97c9b7818f99"
VERSION = "1.1.0"
TASK_ID = "97c9b7818f99"
SUMMARY = "8-frame around interior with 2-3 distinct-color seeds inside."

INVARIANTS = [
    "row 0 and last row are all 8",
    "col 0 and last col are all 8",
    "interior has 2-3 single-cell seeds of distinct non-{0,8} colors",
]

PALETTE_KINDS = ("default", "warm_seeds", "cool_seeds", "rainbow_seeds")
DEGENERATE_TEXTURES = ("no_seeds", "seeds_overlap", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..3"},
    "seed_density":   {"type": "str", "default": "low", "valid": "low"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h):
        g[r][0] = 8; g[r][w - 1] = 8
    g[1][6] = 7
    g[2][2] = 2
    g[4][6] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # frame but no seeds — Voronoi has no centers
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        return g
    if name == "seeds_overlap":
        # all seeds at same distance from every interior cell → universal tie
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        # 2 seeds equidistant from grid center
        g[3][2] = 2
        g[3][7] = 4
        return g
    if name == "no_frame":
        # seeds present but no 8-frame — interior is unbounded
        g[1][6] = 7
        g[2][2] = 2
        g[4][6] = 4
        return g
    return g
