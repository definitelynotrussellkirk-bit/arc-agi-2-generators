"""Generator for arc_puzzle_bank_21_set21_s:S21_E5.

Rule: walls adjacent to red-seeded rooms are highlighted.

Combinatorial axes (8): grid_h/w, room_h, room_w, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_seeds, all_rooms_seeded, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.rooms import center_cell, rectangular_rooms

GENERATOR_ID = "e5ec1ac39df5"
VERSION = "1.1.0"
TASK_ID = "e5ec1ac39df5"
SUMMARY = "Walls adjacent to red-seeded rooms are highlighted."

INVARIANTS = [
    "wall color is 1",
    "floor background is 0",
    "one or two rooms contain red seeds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "all_rooms_seeded", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "room_h":         {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "room_w":         {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        rh = ctx.draw_int("room_h", 3, 3)
        rw = ctx.draw_int("room_w", 3, 3)
    elif difficulty == "hard":
        rh = ctx.draw_int("room_h", 5, 5)
        rw = ctx.draw_int("room_w", 5, 5)
    else:
        rh = ctx.draw_int("room_h", 3, 5)
        rw = ctx.draw_int("room_w", 3, 5)
    grid, rooms = rectangular_rooms(2, 2, rh, rw)
    room_ids = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for room_id in rng.sample(room_ids, rng.randint(1, 2)):
        r, c = center_cell(rooms[room_id[0]][room_id[1]])
        grid[r][c] = 2
    return grid


def _draw_from_degenerate(name, rng):
    grid, rooms = rectangular_rooms(2, 2, 3, 3)
    if name == "no_seeds":
        return grid
    if name == "all_rooms_seeded":
        for ri in range(2):
            for ci in range(2):
                r, c = center_cell(rooms[ri][ci])
                grid[r][c] = 2
        return grid
    if name == "full_grid":
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                grid[r][c] = 1
        return grid
    return grid
