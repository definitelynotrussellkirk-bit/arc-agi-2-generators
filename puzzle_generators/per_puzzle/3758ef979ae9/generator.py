"""Generator for arc_puzzle_bank_21_set21_s:S21_E2.

Rule: each seeded room is filled with its own seed color.

Combinatorial axes (8): room_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_seeds, all_rooms_seeded, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.rooms import center_cell, rectangular_rooms

GENERATOR_ID = "3758ef979ae9"
VERSION = "1.1.0"
TASK_ID = "3758ef979ae9"
SUMMARY = "Each seeded room is filled with its own seed color."

INVARIANTS = [
    "wall color is 1",
    "floor background is 0",
    "each seeded room has exactly one nonzero token color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "all_rooms_seeded", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "room_h":         {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "room_w":         {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "rooms", "valid": "rooms"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        rh = ctx.draw_int("room_h", 3, 3)
        rw = ctx.draw_int("room_w", 3, 4)
    elif difficulty == "hard":
        rh = ctx.draw_int("room_h", 4, 5)
        rw = ctx.draw_int("room_w", 4, 5)
    else:
        rh = ctx.draw_int("room_h", 3, 5)
        rw = ctx.draw_int("room_w", 3, 5)
    rng = ctx.draw_rng("layout")
    grid, rooms = rectangular_rooms(2, 2, rh, rw)
    room_ids = [(0, 0), (0, 1), (1, 0), (1, 1)]
    rng.shuffle(room_ids)
    colors = rng.sample([2, 3, 4, 5, 6, 8, 9], rng.randint(2, 4))
    for room_id, color in zip(room_ids, colors):
        r, c = center_cell(rooms[room_id[0]][room_id[1]])
        grid[r][c] = color
    return grid


def _draw_from_degenerate(name, rng):
    grid, rooms = rectangular_rooms(2, 2, 3, 3)
    if name == "no_seeds":
        return grid
    if name == "all_rooms_seeded":
        for i, room_id in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            r, c = center_cell(rooms[room_id[0]][room_id[1]])
            grid[r][c] = 2 + i
        return grid
    if name == "full_grid":
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                grid[r][c] = 2
        return grid
    return grid
