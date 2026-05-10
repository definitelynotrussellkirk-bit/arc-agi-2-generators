"""Generator for arc_puzzle_bank_21_set21_s:S21_E4.

Rule: only the room with the most green tokens is kept and recolored.

Combinatorial axes (8): room_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_tokens, all_equal, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.rooms import rectangular_rooms

GENERATOR_ID = "1484fc8ec47b"
VERSION = "1.1.0"
TASK_ID = "1484fc8ec47b"
SUMMARY = "Only the room with the most green tokens is kept and recolored."

INVARIANTS = [
    "wall color is 1",
    "floor background is 0",
    "one room has a unique maximum count of color-3 tokens",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_tokens", "all_equal", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "room_h":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "room_w":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rooms", "valid": "rooms"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        rh = ctx.draw_int("room_h", 4, 4)
        rw = ctx.draw_int("room_w", 4, 5)
    elif difficulty == "hard":
        rh = ctx.draw_int("room_h", 5, 6)
        rw = ctx.draw_int("room_w", 5, 6)
    else:
        rh = ctx.draw_int("room_h", 4, 6)
        rw = ctx.draw_int("room_w", 4, 6)
    rng = ctx.draw_rng("layout")
    grid, rooms = rectangular_rooms(2, 2, rh, rw)
    room_ids = [(0, 0), (0, 1), (1, 0), (1, 1)]
    target = rng.choice(room_ids)
    for room_id in room_ids:
        room = rooms[room_id[0]][room_id[1]]
        n = 4 if room_id == target else rng.randint(0, 2)
        for r, c in rng.sample(room["cells"], n):
            grid[r][c] = 3
    return grid


def _draw_from_degenerate(name, rng):
    grid, rooms = rectangular_rooms(2, 2, 4, 4)
    if name == "no_tokens":
        return grid
    if name == "all_equal":
        for room_id in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            room = rooms[room_id[0]][room_id[1]]
            r, c = room["cells"][0]
            grid[r][c] = 3
        return grid
    if name == "full_grid":
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                grid[r][c] = 3
        return grid
    return grid
