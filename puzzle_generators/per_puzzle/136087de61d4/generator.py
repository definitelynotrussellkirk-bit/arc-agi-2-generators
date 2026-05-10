"""Generator for arc_puzzle_bank_21_set6_s:S6_H7.

Rule: two matching markers are connected by the shortest route through
zero cells while 9-cells act as walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_endpoint, blocked_path, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "136087de61d4"
VERSION = "1.1.0"
TASK_ID = "136087de61d4"
SUMMARY = "Draw the shortest zero-cell path between two markers around 9-walls."

INVARIANTS = [
    "there are exactly two color-3 endpoints",
    "color 9 cells are walls",
    "a zero-cell path exists between the endpoints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_endpoint", "blocked_path", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "endpoints_corners",
                       "valid": "endpoints_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    left_wall = rng.randint(4, max(4, w // 2))
    right_wall = rng.randint(left_wall + 3, w - 3)
    gap_a = rng.randint(1, h - 2)
    gap_b = rng.randint(1, h - 2)
    for r in range(h):
        if r != gap_a:
            g[r][left_wall] = 9
        if r != gap_b:
            g[r][right_wall] = 9
    g[1][1] = 3
    g[h - 2][w - 2] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    left_wall = 5
    right_wall = 9
    if name == "missing_endpoint":
        # only one color-3 marker → rule needs two, path is undefined
        for r in range(h):
            if r != 3:
                g[r][left_wall] = 9
        g[1][1] = 3
        return g
    if name == "blocked_path":
        # walls fully enclose one endpoint → no zero-cell path between markers
        for r in range(h):
            g[r][left_wall] = 9
        g[1][1] = 3
        g[h - 2][w - 2] = 3
        return g
    if name == "no_walls":
        # endpoints with no walls → shortest path is a straight Manhattan corridor
        g[1][1] = 3
        g[h - 2][w - 2] = 3
        return g
    return g
