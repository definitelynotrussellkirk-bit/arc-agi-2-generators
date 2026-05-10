"""Generator for arc_puzzle_bank_fifteenth21:M103.

Color-1 walls divide the grid into rooms. Each room contains one colored seed;
the rule fills that room's zeros with the seed color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, layout,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multiple_seeds_per_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bfef8519fe18"
VERSION = "1.1.0"
TASK_ID = "bfef8519fe18"
SUMMARY = "Color-1 walls enclose seeded rooms whose empty cells are filled."

INVARIANTS = [
    "color 1 is the wall color",
    "every non-wall connected region contains exactly one seed color",
    "seed colors are nonzero and not 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multiple_seeds_per_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "auto", "valid": "auto"},
    "grid_w":         {"type": "int", "default": "auto", "valid": "auto"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "layout":         {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "room_h":         {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "room_w":         {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "wall1_rooms_with_seeds",
                       "valid": "wall1_rooms_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LAYOUTS = [(2, 2), (2, 3), (3, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        room_rows, room_cols = _LAYOUTS[ctx.draw_int("layout", 0, 0)]
        room_h = ctx.draw_int("room_h", 2, 2)
        room_w = ctx.draw_int("room_w", 3, 3)
    elif difficulty == "hard":
        room_rows, room_cols = _LAYOUTS[ctx.draw_int("layout", 1, 2)]
        room_h = ctx.draw_int("room_h", 3, 3)
        room_w = ctx.draw_int("room_w", 4, 4)
    else:
        room_rows, room_cols = _LAYOUTS[ctx.draw_int("layout", 0, 2)]
        room_h = ctx.draw_int("room_h", 2, 3)
        room_w = ctx.draw_int("room_w", 3, 4)
    h = room_rows * room_h + room_rows + 1
    w = room_cols * room_w + room_cols + 1
    g = full_grid(h, w, 1)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], room_rows * room_cols)
    color_idx = 0
    for rr in range(room_rows):
        top = 1 + rr * (room_h + 1)
        for cc in range(room_cols):
            left = 1 + cc * (room_w + 1)
            for r in range(top, top + room_h):
                for c in range(left, left + room_w):
                    g[r][c] = 0
            seed_r = rng.randint(top, top + room_h - 1)
            seed_c = rng.randint(left, left + room_w - 1)
            g[seed_r][seed_c] = colors[color_idx]
            color_idx += 1
    return g


def _draw_from_degenerate(name, rng):
    room_rows, room_cols = 2, 2
    room_h, room_w = 3, 4
    h = room_rows * room_h + room_rows + 1
    w = room_cols * room_w + room_cols + 1
    if name == "no_walls":
        # seeds but no color-1 walls → single open region, all seeds compete
        g = full_grid(h, w, 0)
        g[2][2] = 4; g[2][7] = 6; g[6][2] = 7; g[6][7] = 8
        return g
    if name == "no_seeds":
        # walls present but no seeds → no fill color defined for any room
        g = full_grid(h, w, 1)
        for rr in range(room_rows):
            top = 1 + rr * (room_h + 1)
            for cc in range(room_cols):
                left = 1 + cc * (room_w + 1)
                for r in range(top, top + room_h):
                    for c in range(left, left + room_w):
                        g[r][c] = 0
        return g
    if name == "multiple_seeds_per_room":
        # 2 distinct seeds in one room → ambiguous fill color
        g = full_grid(h, w, 1)
        for rr in range(room_rows):
            top = 1 + rr * (room_h + 1)
            for cc in range(room_cols):
                left = 1 + cc * (room_w + 1)
                for r in range(top, top + room_h):
                    for c in range(left, left + room_w):
                        g[r][c] = 0
        # room (0,0) has 2 seeds
        g[1][1] = 4; g[2][3] = 6
        g[1][6] = 7
        g[5][1] = 8
        return g
    return full_grid(h, w, 0)
