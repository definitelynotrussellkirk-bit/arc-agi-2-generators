"""Generator for arc_additional_puzzle_bank_volume11:H73 — top-row radius controls cyan dilation.

Rule: a top-row radius controls cyan dilation from the red seed
component through non-wall cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, radius,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_radius, no_seed, sealed_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bd2a79b78c01"
VERSION = "1.1.0"
TASK_ID = "bd2a79b78c01"
SUMMARY = "A top-row radius controls cyan dilation from the red seed component through non-wall cells."

INVARIANTS = [
    "the first top-row value in 1..3 is the dilation radius",
    "gray cells are walls",
    "red seed cells are connected",
    "the seed component has reachable background within and beyond the radius",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_radius", "no_seed", "sealed_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "radius":         {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "radius_with_walls_and_seed",
                       "valid": "radius_with_walls_and_seed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        radius = ctx.draw_int("radius", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 16)
        radius = ctx.draw_int("radius", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 11, 16)
        radius = ctx.draw_int("radius", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = radius if radius != 2 else 3
    wall_col = rng.randint(4, w - 5)
    gap = rng.randint(3, h - 3)
    for r in range(1, h - 1):
        if r != gap:
            g[r][wall_col] = 5
    for c in range(1, wall_col):
        if c not in {2, wall_col - 1}:
            g[h - 3][c] = 5
    sr = rng.randint(2, min(h - 4, gap + 1))
    sc = rng.randint(1, max(1, wall_col - 3))
    g[sr][sc] = 2
    g[sr][sc + 1] = 2
    g[sr + 1][sc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_radius":
        # walls + seed but (0,0) is bg → no dilation radius specified
        for r in range(1, h - 1): g[r][6] = 5
        g[3][2] = 2; g[3][3] = 2; g[4][2] = 2
        return g
    if name == "no_seed":
        # radius + walls but no red seed → nothing to dilate from
        g[0][0] = 2
        for r in range(1, h - 1): g[r][6] = 5
        return g
    if name == "sealed_chamber":
        # seed sealed by walls so dilation reaches nothing
        g[0][0] = 2
        for r in range(h):
            g[r][5] = 5
        for c in range(w):
            g[3][c] = 5
        g[1][2] = 2; g[1][3] = 2; g[2][2] = 2   # seed in tiny enclosed chamber
        return g
    return g
