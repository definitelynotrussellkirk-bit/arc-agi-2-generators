"""Generator for arc_additional_puzzle_bank_volume14:H93.

Rule: three seed colors compete by wall-aware shortest path, with
nearest ties left blank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, no_walls, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "88c2677d619b"
VERSION = "1.1.0"
TASK_ID = "88c2677d619b"
SUMMARY = "Three seed colors compete by wall-aware shortest path, with nearest ties left blank."

INVARIANTS = [
    "background is 0",
    "wall color is 5",
    "one seed of each color 1, 2, and 3 is present",
    "the maze creates distinct nearest regions and possible ties",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "walled_corners",
                       "valid": "walled_corners"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "walled", "valid": "walled"},
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
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 11, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    wall_col = w // 2
    gap = rng.randint(2, h - 3)
    for r in range(1, h - 1):
        if r != gap:
            g[r][wall_col] = 5
    for c in range(1, wall_col + 1):
        if c != wall_col - 1:
            g[h // 2][c] = 5
    g[1][2] = 1
    g[h - 2][2] = 2
    g[rng.randint(1, h - 2)][w - 3] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # walls but no seeds → voronoi has no sources
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        return g
    if name == "no_walls":
        # seeds without walls → wall-aware distance reduces to plain Manhattan
        g[1][2] = 1
        g[h - 2][2] = 2
        g[3][w - 3] = 3
        return g
    if name == "single_seed":
        # one seed → entire reachable interior is its color, no ties possible
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        g[3][3] = 1
        return g
    return g
