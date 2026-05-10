"""Generator for arc_puzzle_bank_21_set11_bundle:hard_k17 — BFS through 8-walled maze with key/door.

Rule: 8-walled outer + interior walls. Start (2), goal (3), color-4 key,
color-5 door (passable only with key). Output paints the BFS path color 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_start, door_without_key, walls_block_path.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "671a9af906aa"
VERSION = "1.1.0"
TASK_ID = "671a9af906aa"

SUMMARY = "8-walled grid + start (2), goal (3), 0-1 key (4), 0-2 doors (5), interior walls."

INVARIANTS = [
    "background is 0",
    "outer border is color-8 walls",
    "exactly one color-2 start and one color-3 goal cell, both interior",
    "0-1 color-4 key cell, 0-2 color-5 door cells",
    "some interior color-8 wall cells (sparse)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_start", "door_without_key", "walls_block_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "use_key":        {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "n_doors":        {"type": "int", "default": "rng 0..2", "valid": "0..3"},
    "n_iw":           {"type": "int", "default": "rng 0..2", "valid": "0..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "walled_maze_with_keys",
                       "valid": "walled_maze_with_keys"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
        use_key = ctx.draw_int("use_key", 0, 0)
        n_doors = ctx.draw_int("n_doors", 0, 1)
        n_iw = ctx.draw_int("n_iw", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        use_key = ctx.draw_int("use_key", 1, 1)
        n_doors = ctx.draw_int("n_doors", 2, 3)
        n_iw = ctx.draw_int("n_iw", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        use_key = ctx.draw_int("use_key", 0, 1)
        n_doors = ctx.draw_int("n_doors", 0, 2)
        n_iw = ctx.draw_int("n_iw", 0, 2)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8

    def place(value):
        for _ in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = value
            return (r, c)
        return None

    s = place(2)
    if s is None: return g
    for _ in range(120):
        gr = rng.randint(1, h - 2); gc = rng.randint(1, w - 2)
        if g[gr][gc] != 0: continue
        if abs(gr - s[0]) + abs(gc - s[1]) < 4: continue
        g[gr][gc] = 3; break
    if n_doors > 0:
        use_key = 1
    if use_key:
        place(4)
    for _ in range(n_doors):
        place(5)
    for _ in range(n_iw):
        place(8)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8
    if name == "no_start":
        # Goal but no start — rule's BFS has no source; path
        # undefined.
        g[5][7] = 3
        return g
    if name == "door_without_key":
        # Door present but no key — rule's "passable with key"
        # branch never activates; door is effectively a wall.
        g[1][1] = 2; g[5][7] = 3; g[3][4] = 5
        return g
    if name == "walls_block_path":
        # Walls form a column that disconnects start side from
        # goal side — rule's BFS yields no path.
        g[1][1] = 2; g[5][7] = 3
        for r in range(1, h - 1): g[r][4] = 8
        return g
    return g
