"""Generator for arc_puzzle_bank_21_set21_s:S21_E1.

Rule: one wall-bounded room contains a red seed and is filled.

Combinatorial axes (8): grid_h/w, room_h, room_w, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_seed, no_walls, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.rooms import center_cell, rectangular_rooms

GENERATOR_ID = "4c1d80c25a99"
VERSION = "1.1.0"
TASK_ID = "4c1d80c25a99"
SUMMARY = "One wall-bounded room contains a red seed and is filled."

INVARIANTS = [
    "wall color is 1",
    "floor background is 0",
    "exactly one room contains a color-2 seed",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "no_walls", "full_grid")
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
    target = rng.choice([(0, 0), (0, 1), (1, 0), (1, 1)])
    r, c = center_cell(rooms[target[0]][target[1]])
    grid[r][c] = 2
    return grid


def _draw_from_degenerate(name, rng):
    grid, rooms = rectangular_rooms(2, 2, 3, 3)
    if name == "no_seed":
        return grid
    if name == "no_walls":
        h, w = len(grid), len(grid[0])
        empty = [[0] * w for _ in range(h)]
        empty[3][3] = 2
        return empty
    if name == "full_grid":
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                grid[r][c] = 1
        return grid
    return grid
