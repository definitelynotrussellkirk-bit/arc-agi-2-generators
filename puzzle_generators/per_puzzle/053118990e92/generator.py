"""Generator for arc_additional_puzzles_21_set20_bundle:H137 — Voronoi inside 8-frame.

Rule: 8-frame surrounds interior; non-zero non-8 cells are seeds. Fill
each empty cell with nearest seed's color (ties → 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, single_seed, broken_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "053118990e92"
VERSION = "1.1.0"
TASK_ID = "053118990e92"
SUMMARY = "8-frame around interior with 2-3 distinct-color single-cell seeds."

INVARIANTS = [
    "8-frame on outer border (rectangular)",
    "interior has 2-3 single-cell seeds of distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "broken_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "8frame_with_voronoi_seeds",
                       "valid": "8frame_with_voronoi_seeds"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    for c in range(2, w - 2):
        g[1][c] = 8; g[h - 2][c] = 8
    for r in range(1, h - 1):
        g[r][2] = 8; g[r][w - 3] = 8
    palette = [2, 3, 4, 5, 6, 7]; rng.shuffle(palette)
    placed = 0
    n = rng.randint(2, 3)
    while placed < n:
        sr = rng.randint(2, h - 3); sc = rng.randint(3, w - 4)
        if g[sr][sc] == 0:
            g[sr][sc] = palette[placed]; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    for c in range(2, w - 2):
        g[1][c] = 8; g[h - 2][c] = 8
    for r in range(1, h - 1):
        g[r][2] = 8; g[r][w - 3] = 8
    if name == "no_seeds":
        # frame but no seeds → no Voronoi sources, interior stays empty
        return g
    if name == "single_seed":
        # 1 seed → entire interior becomes that color (no signal of distance)
        g[4][5] = 4
        return g
    if name == "broken_frame":
        # frame has gap → "interior" is connected to outside (Voronoi escapes)
        g[1][5] = 0   # gap in top edge
        g[3][4] = 4
        g[5][7] = 6
        return g
    return g
