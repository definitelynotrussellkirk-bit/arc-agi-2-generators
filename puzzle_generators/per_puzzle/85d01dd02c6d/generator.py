"""Generator for arc_additional_puzzles_21_set12_bundle:H82 — Mark cells visible from ≥2 seeds inside 9-frame.

Rule: 9-frame surrounds interior. For each empty cell, count seeds with
clear LoS (row or col, no 9 between). If ≥2 → 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, single_seed, no_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "85d01dd02c6d"
VERSION = "1.1.0"
TASK_ID = "85d01dd02c6d"
SUMMARY = "9-frame around interior with 2-3 single-cell seeds."

INVARIANTS = [
    "9-frame on outer border",
    "interior has 2-3 single-cell seeds of distinct non-{0,9} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "9frame_with_2_3_seeds",
                       "valid": "9frame_with_2_3_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    for c in range(w):
        g[0][c] = 9; g[h - 1][c] = 9
    for r in range(h):
        g[r][0] = 9; g[r][w - 1] = 9
    palette = [2, 3, 4, 6, 7, 8]; rng.shuffle(palette)
    n = rng.randint(2, 3)
    placed = 0
    while placed < n:
        sr = rng.randint(2, h - 3); sc = rng.randint(2, w - 3)
        if g[sr][sc] == 0:
            g[sr][sc] = palette[placed]; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 9; g[h - 1][c] = 9
    for r in range(h): g[r][0] = 9; g[r][w - 1] = 9
    if name == "no_seeds":
        # frame but no seeds → no LoS sources, no cells get marked
        return g
    if name == "single_seed":
        # only 1 seed → no cell can have ≥2 seeds visible
        g[3][5] = 4
        return g
    if name == "no_frame":
        # seeds present but no 9-frame → "interior" undefined, LoS rule has no walls
        g2 = full_grid(h, w, 0)
        g2[3][3] = 4; g2[5][7] = 6
        return g2
    return g
