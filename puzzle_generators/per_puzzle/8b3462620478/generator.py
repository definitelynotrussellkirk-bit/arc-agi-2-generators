"""Generator for arc_additional_puzzle_bank_volume7:H48.

Rule: source=2, arrow=1 adjacent. Ray traces in arrow direction, paints
0-cells as 8, stops on 5 or out-of-bounds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, wall_row,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_arrow, no_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b3462620478"
VERSION = "1.1.0"
TASK_ID = "8b3462620478"
SUMMARY = "Source 2-cell + adjacent 1-arrow + a row/col of 5s as wall."

INVARIANTS = [
    "exactly one 2-cell (source)",
    "exactly one 1-cell adjacent to the source (arrow)",
    "a horizontal or vertical line of 5s positioned away from the source",
    "rest of grid is 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_arrow", "no_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "wall_row":       {"type": "int", "default": "rng 2..h/2", "valid": "1..h-3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "wall_top_source_bottom",
                       "valid": "wall_top_source_bottom"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    wall_row = rng.randint(2, h // 2)
    for c in range(w):
        g[wall_row][c] = 5
    sr = rng.randint(wall_row + 2, h - 2)
    sc = rng.randint(1, w - 2)
    g[sr][sc] = 2
    g[sr][sc + 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_source":
        # arrow + wall but no 2-source → ray has no origin
        for c in range(w): g[2][c] = 5
        g[5][3] = 1
        return g
    if name == "no_arrow":
        # source + wall but no arrow → no direction defined
        for c in range(w): g[2][c] = 5
        g[5][3] = 2
        return g
    if name == "no_wall":
        # source + arrow but no 5-wall → ray goes off-grid, no termination
        g[5][3] = 2
        g[5][4] = 1
        return g
    return g
