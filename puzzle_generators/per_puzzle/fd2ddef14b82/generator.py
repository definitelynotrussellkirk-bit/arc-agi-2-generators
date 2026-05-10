"""Generator for arc_puzzle_bank_21_set14_bundle:hard_n05 — BFS with single key/door.

Rule: start=2, goal=3, walls=5, color 7 = door (need key 6 to pass). Output
paints the shortest path in color 4 (or returns input if unreachable).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: door_without_key (door (7) present but no key (6) → rule's
key-acquired branch never fires, path is blocked at door), no_walls
(no obstacles → BFS reduces to Manhattan distance, no rule branches),
no_path (walls fully encircle goal → rule's "unreachable" branch
fires, output equals input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fd2ddef14b82"
VERSION = "1.1.0"
TASK_ID = "fd2ddef14b82"

SUMMARY = "Start (2), goal (3), 0-3 walls (5), 0-1 key (6), 0-2 doors (7)."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 start and one color-3 goal cell",
    "0-4 color-5 wall cells",
    "0-1 color-6 key cell, 0-2 color-7 door cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("door_without_key", "no_walls", "no_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "10..16"},
    "n_walls":        {"type": "int", "default": "rng 0..4", "valid": "0..6"},
    "use_key":        {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "n_doors":        {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "start_goal_walls_keys_doors",
                       "valid": "start_goal_walls_keys_doors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 10)
        n_walls = ctx.draw_int("n_walls", 0, 1)
        use_key = ctx.draw_int("use_key", 0, 0)
        n_doors = ctx.draw_int("n_doors", 0, 0)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 15)
        n_walls = ctx.draw_int("n_walls", 3, 5)
        use_key = ctx.draw_int("use_key", 1, 1)
        n_doors = ctx.draw_int("n_doors", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n_walls = ctx.draw_int("n_walls", 0, 4)
        use_key = ctx.draw_int("use_key", 0, 1)
        n_doors = ctx.draw_int("n_doors", 0, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        sr = rng.randint(0, h - 1); sc = rng.randint(0, w - 1)
        g[sr][sc] = 2
        for _ in range(120):
            gr = rng.randint(0, h - 1); gc = rng.randint(0, w - 1)
            if (gr, gc) == (sr, sc): continue
            if abs(gr - sr) + abs(gc - sc) < 4: continue
            g[gr][gc] = 3
            break
        else:
            continue
        for _ in range(n_walls):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = 5
                break
        if use_key:
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = 6
                break
        for _ in range(n_doors):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                g[r][c] = 7
                break
        return g
    raise ValueError("could not realize set14 n05 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "door_without_key":
        # Door (7) present but no key (6) — rule's key-acquired
        # branch never fires; path is blocked at the door.
        g[1][1] = 2
        g[7][9] = 3
        for r in range(2, 7): g[r][5] = 5
        g[4][5] = 7
        return g
    if name == "no_walls":
        # No obstacles — BFS reduces to Manhattan distance; rule's
        # wall-handling branch never fires.
        g[1][1] = 2
        g[7][9] = 3
        return g
    if name == "no_path":
        # Walls fully encircle the goal — rule's "unreachable"
        # branch fires, output equals input.
        g[1][1] = 2
        g[5][5] = 3
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            g[5 + dr][5 + dc] = 5
        return g
    return g
