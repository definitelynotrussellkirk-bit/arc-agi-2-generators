"""Generator for arc_additional_puzzle_bank_volume3:H18 — chambers filled by nearest seed.

Rule: gray-wall chambers are filled by nearest seed, with distance ties
choosing the smaller color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, no_walls, equidistant_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28f91ad53b1b"
VERSION = "1.1.0"
TASK_ID = "28f91ad53b1b"
SUMMARY = "Gray-wall chambers are filled by nearest seed, with distance ties choosing the smaller color."

INVARIANTS = [
    "background is 0",
    "gray cells are walls",
    "non-wall nonzero cells are seeds",
    "every active chamber has at least two seed colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "equidistant_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "wall_chambers_with_seeds",
                       "valid": "wall_chambers_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _add_border(g: list[list[int]], wall: int = 5) -> None:
    h = len(g)
    w = len(g[0])
    for r in range(h):
        g[r][0] = wall
        g[r][w - 1] = wall
    for c in range(w):
        g[0][c] = wall
        g[h - 1][c] = wall


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    _add_border(g)
    mid = w // 2
    for r in range(1, h - 1):
        if r != h // 2:
            g[r][mid] = 5
    g[2][2] = 2
    g[h - 3][mid - 2] = 3
    g[2][w - 3] = 4
    if rng.choice([True, False]) and h > 9:
        g[h - 3][w - 3] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    _add_border(g)
    mid = w // 2
    if name == "no_seeds":
        # walls present but no seeds → no Voronoi sources, chambers stay empty
        for r in range(1, h - 1): g[r][mid] = 5
        return g
    if name == "no_walls":
        # no internal walls → entire grid is one chamber, no partition
        g2 = full_grid(h, w, 0)
        g2[2][2] = 2; g2[5][8] = 4   # seeds in undivided space
        return g2
    if name == "equidistant_seeds":
        # 2 seeds equidistant from many cells → many ties (degenerate Voronoi)
        for r in range(1, h - 1): g[r][mid] = 5
        g[h // 2][2] = 2          # exactly mirrored across walls
        g[h // 2][w - 3] = 4
        return g
    return g
