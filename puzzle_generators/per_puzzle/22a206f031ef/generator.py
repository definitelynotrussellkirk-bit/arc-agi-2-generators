"""Generator for arc_puzzle_bank_21_set18_bundle:hard_p05 — flood-fill rooms by color seeds.

Rule: outer color-5 walls bound the grid; some interior color-5 walls divide
it into rooms. Each colored seed (non-{0, 5}) flood-fills its connected
component (over 0-cells), painting the room in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_walls, n_seeds, texture.
Degenerates: no_walls, no_seeds, multi_seeds_per_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "22a206f031ef"
VERSION = "1.1.0"
TASK_ID = "22a206f031ef"

SUMMARY = "5-walled outer border + 0-2 interior walls + 1-3 colored seeds in each room."

INVARIANTS = [
    "background is 0",
    "outer border is color-5 walls",
    "0-2 interior color-5 walls (full row or column segments) partition the interior",
    "1-3 single-cell seeds in distinct non-{0, 5} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multi_seeds_per_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "n_seeds":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_seeds+2", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "walled_rooms_with_seeds",
                       "valid": "walled_rooms_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "= n_seeds+2", "valid": "3..6"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        n_walls = ctx.draw_int("n_walls", 0, 1)
        n_seeds = ctx.draw_int("n_seeds", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 16)
        n_walls = ctx.draw_int("n_walls", 2, 3)
        n_seeds = ctx.draw_int("n_seeds", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
        n_walls = ctx.draw_int("n_walls", 0, 2)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h): g[r][0] = 5; g[r][w - 1] = 5
    for _ in range(n_walls):
        if rng.choice([True, False]):
            r = rng.randint(2, h - 3)
            for c in range(1, w - 1): g[r][c] = 5
            door_c = rng.randint(1, w - 2)
            g[r][door_c] = 0
        else:
            c = rng.randint(2, w - 3)
            for r in range(1, h - 1): g[r][c] = 5
            door_r = rng.randint(1, h - 2)
            g[door_r][c] = 0
    seed_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_seeds)
    for color in seed_colors:
        for _t in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h): g[r][0] = 5; g[r][w - 1] = 5
    if name == "no_walls":
        # Outer-only border + multi-color seeds — every seed is in
        # the SAME room; rule's per-room paint becomes ambiguous
        # (multiple seeds in one room).
        g[3][3] = 4; g[5][7] = 6; g[6][2] = 7
        return g
    if name == "no_seeds":
        # Walls + rooms but no seeds — rule has no color to paint
        # any room with.
        for c in range(1, w - 1): g[4][c] = 5
        return g
    if name == "multi_seeds_per_room":
        # Wall divider + multiple distinct-colored seeds in the SAME
        # half — rule's "single seed per room" precondition fails;
        # fill color is ambiguous.
        for c in range(1, w - 1): g[4][c] = 5
        g[4][5] = 0
        g[2][3] = 3; g[2][7] = 6
        g[6][4] = 8; g[6][8] = 9
        return g
    return g
