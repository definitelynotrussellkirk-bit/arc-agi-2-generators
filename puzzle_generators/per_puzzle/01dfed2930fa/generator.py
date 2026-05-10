"""Generator for arc_puzzle_bank_21_set20_bundle:medium_p05 — room fill from doors.

Rule: 8-walls divide grid into rooms. Each room has exactly one seed
(non-bg, non-8). Fill the room interior with that seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rooms,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multi_color_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "01dfed2930fa"
VERSION = "1.1.0"
TASK_ID = "01dfed2930fa"
SUMMARY = "8-bordered grid with one internal vertical 8-wall, two rooms each with one seed."

INVARIANTS = [
    "background is 0",
    "outer border is all 8",
    "exactly one internal 8-wall column dividing into 2 rooms",
    "each room has one non-bg, non-8 seed cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multi_color_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rooms":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_with_vertical_split",
                       "valid": "border_with_vertical_split"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h):
        g[r][0] = 8; g[r][w - 1] = 8
    wall_c = rng.randint(3, w - 4)
    for r in range(h):
        g[r][wall_c] = 8
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 2)
    sl = (rng.randint(1, h - 2), rng.randint(1, wall_c - 1))
    sr = (rng.randint(1, h - 2), rng.randint(wall_c + 1, w - 2))
    g[sl[0]][sl[1]] = palette[0]
    g[sr[0]][sr[1]] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # seeds but no walls → no rooms defined
        g[2][3] = 4
        g[5][6] = 6
        return g
    if name == "no_seeds":
        # walls form rooms but no seeds → no color to fill rooms with
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        for r in range(h): g[r][5] = 8
        return g
    if name == "multi_color_room":
        # one room has 2 different seed colors → ambiguous fill color
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        for r in range(h): g[r][5] = 8
        g[2][2] = 4; g[3][3] = 6   # two colors in left room
        g[5][7] = 7
        return g
    return g
