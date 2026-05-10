"""Generator for arc_puzzle_bank_21_set18_bundle:medium_p01 — fill each seeded room.

Rule: 5-walls divide the grid into rooms. Each room has exactly one
non-bg non-5 seed. Fill the room with that seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, both_seeds_in_one_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "423fca3dc076"
VERSION = "1.1.0"
TASK_ID = "423fca3dc076"
SUMMARY = "5-bordered grid with one internal wall, two rooms each holding one seed."

INVARIANTS = [
    "background is 0",
    "outer border is all 5",
    "exactly one internal 5-wall column or row dividing the interior into 2 rooms",
    "each room contains exactly one non-bg, non-5 seed cell",
    "rooms have distinct seed colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "both_seeds_in_one_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "1", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "framed_two_rooms",
                       "valid": "framed_two_rooms"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "framed", "valid": "framed"},
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
        h = ctx.draw_int("grid_h", 8, 8)
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
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    wall_c = rng.randint(3, w - 4)
    for r in range(h):
        g[r][wall_c] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    sl = (rng.randint(1, h - 2), rng.randint(1, wall_c - 1))
    sr = (rng.randint(1, h - 2), rng.randint(wall_c + 1, w - 2))
    g[sl[0]][sl[1]] = palette[0]
    g[sr[0]][sr[1]] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    if name == "no_walls":
        # bordered grid with no interior wall → only one room, predicate "two rooms" fails
        g[3][3] = 4; g[5][7] = 6   # two seeds in same room
        return g
    if name == "no_seeds":
        # walls but no seeds → rooms empty, rule has nothing to fill
        wall_c = w // 2
        for r in range(h):
            g[r][wall_c] = 5
        return g
    if name == "both_seeds_in_one_room":
        # walls present, but both seeds in same room → predicate "one seed per room" fails
        wall_c = w // 2
        for r in range(h):
            g[r][wall_c] = 5
        g[2][2] = 4; g[5][3] = 6   # both in left room
        return g
    return g
