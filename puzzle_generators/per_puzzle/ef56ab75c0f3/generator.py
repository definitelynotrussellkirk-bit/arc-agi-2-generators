"""Generator for arc_puzzle_bank_21_set23_bundle:hard_p02 — BFS through 2-key maze.

Rule: 4-walled grid. Start (2), goal (3). Color 5 = key1 pickup, color 6 =
door1 (needs key1). Color 7 = key2 pickup, color 8 = door2 (needs key2).
Output paints the BFS path color 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_iw,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_start, no_goal, walled_off.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef56ab75c0f3"
VERSION = "1.1.0"
TASK_ID = "ef56ab75c0f3"

SUMMARY = "4-walled grid + start (2), goal (3), 0-1 each of keys 5/7 and doors 6/8."

INVARIANTS = [
    "background is 0",
    "outer border is color-4 walls",
    "exactly one color-2 start and one color-3 goal cell, both interior",
    "0-1 color-5 key1 / color-6 door1, 0-1 color-7 key2 / color-8 door2",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_start", "no_goal", "walled_off")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "use_k1":         {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "use_k2":         {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "n_iw":           {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "3..9"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "3..9"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        use_k1 = ctx.draw_int("use_k1", 0, 1)
        use_k2 = ctx.draw_int("use_k2", 0, 0)
        n_iw = ctx.draw_int("n_iw", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        use_k1 = ctx.draw_int("use_k1", 1, 1)
        use_k2 = ctx.draw_int("use_k2", 1, 1)
        n_iw = ctx.draw_int("n_iw", 1, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        use_k1 = ctx.draw_int("use_k1", 0, 1)
        use_k2 = ctx.draw_int("use_k2", 0, 1)
        n_iw = ctx.draw_int("n_iw", 0, 2)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 4; g[h - 1][c] = 4
    for r in range(h): g[r][0] = 4; g[r][w - 1] = 4

    def place(value):
        for _ in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = value
            return (r, c)
        return None

    s = place(2)
    if s is None: return g
    for _t in range(120):
        r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
        if g[r][c] != 0: continue
        if abs(r - s[0]) + abs(c - s[1]) < 4: continue
        g[r][c] = 3; break
    if use_k1:
        place(5); place(6)
    if use_k2:
        place(7); place(8)
    for _ in range(n_iw):
        place(4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 4; g[h - 1][c] = 4
    for r in range(h): g[r][0] = 4; g[r][w - 1] = 4
    if name == "no_start":
        # No color-2 start cell — rule has no source to BFS from.
        g[3][3] = 3
        return g
    if name == "no_goal":
        # No color-3 goal cell — rule has no destination.
        g[3][3] = 2
        return g
    if name == "walled_off":
        # Goal isolated by interior walls — no BFS path exists.
        g[3][3] = 2
        g[5][7] = 3
        for c in range(1, w - 1): g[4][c] = 4
        return g
    return g
