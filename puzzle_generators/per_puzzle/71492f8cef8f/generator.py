"""Generator for arc_puzzle_bank_sixteenth21:M112 — fill rooms from unique seeds.

Rule: 5-walls divide grid into rooms. Each room with exactly one
non-{0,5} seed gets filled with the seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rooms,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multi_color_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "71492f8cef8f"
VERSION = "1.1.0"
TASK_ID = "71492f8cef8f"
SUMMARY = "5-bordered grid with horizontal 5-wall, two rooms each holding one seed."

INVARIANTS = [
    "background is 0",
    "outer border is all 5",
    "exactly one internal horizontal 5-wall dividing into 2 rooms",
    "each room has one non-{0,5} seed cell, distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multi_color_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rooms":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_with_horizontal_split",
                       "valid": "border_with_horizontal_split"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    wall_r = rng.randint(2, h - 4)
    for c in range(w):
        g[wall_r][c] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    sa = (rng.randint(1, wall_r - 1), rng.randint(1, w - 2))
    sb = (rng.randint(wall_r + 1, h - 2), rng.randint(1, w - 2))
    g[sa[0]][sa[1]] = palette[0]
    g[sb[0]][sb[1]] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # seeds but no walls → no rooms defined, no flood scope
        g[2][3] = 4
        g[5][6] = 6
        return g
    if name == "no_seeds":
        # walls form rooms but no seeds → no color to fill rooms with
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w): g[4][c] = 5
        return g
    if name == "multi_color_room":
        # one room has TWO different seed colors → ambiguous fill color
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w): g[4][c] = 5
        g[2][2] = 4; g[3][6] = 6   # two colors in same (top) room
        g[6][3] = 7
        return g
    return g
