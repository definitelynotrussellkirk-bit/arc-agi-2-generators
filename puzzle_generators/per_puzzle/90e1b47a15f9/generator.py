"""Generator for arc_puzzle_bank_21_set15_bundle:hard_o03 — BFS through 2-key maze.

Rule: start=2, goal=3, walls=8. Picking up color 4 unlocks doors of color 6;
picking up color 5 unlocks doors of color 7. Output traces the path in
color 9 (or empty grid if unreachable).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: door_without_key (door (6) present but no key (4) → rule's
unlock branch never fires, path blocked), no_walls (only border walls →
BFS reduces to Manhattan distance, no rule branches), no_path (interior
walls fully encircle goal → rule's "unreachable" branch fires, output
empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "90e1b47a15f9"
VERSION = "1.1.0"
TASK_ID = "90e1b47a15f9"

SUMMARY = "Walled grid (8) with start (2), goal (3), keys (4, 5), doors (6, 7), some interior walls."

INVARIANTS = [
    "background is 0",
    "outer border is color-8 walls",
    "exactly one color-2 start cell and one color-3 goal cell, both interior",
    "0-2 color-4 key A cells and 0-2 color-6 door cells",
    "0-2 color-5 key B cells and 0-2 color-7 door cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("door_without_key", "no_walls", "no_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "n_keys_a":       {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "n_keys_b":       {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "n_doors_a":      {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "n_doors_b":      {"type": "int", "default": "rng 0..1", "valid": "0..2"},
    "n_interior_walls": {"type": "int", "default": "rng 0..3", "valid": "0..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "walled_maze_with_keys_doors",
                       "valid": "walled_maze_with_keys_doors"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
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
        w = ctx.draw_int("grid_w", 10, 10)
        n_ka = ctx.draw_int("n_keys_a", 0, 0)
        n_kb = ctx.draw_int("n_keys_b", 0, 0)
        n_da = ctx.draw_int("n_doors_a", 0, 0)
        n_db = ctx.draw_int("n_doors_b", 0, 0)
        n_iw = ctx.draw_int("n_interior_walls", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 15)
        n_ka = ctx.draw_int("n_keys_a", 1, 2)
        n_kb = ctx.draw_int("n_keys_b", 1, 2)
        n_da = ctx.draw_int("n_doors_a", 1, 2)
        n_db = ctx.draw_int("n_doors_b", 1, 2)
        n_iw = ctx.draw_int("n_interior_walls", 2, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 10, 13)
        n_ka = ctx.draw_int("n_keys_a", 0, 1)
        n_kb = ctx.draw_int("n_keys_b", 0, 1)
        n_da = ctx.draw_int("n_doors_a", 0, 1)
        n_db = ctx.draw_int("n_doors_b", 0, 1)
        n_iw = ctx.draw_int("n_interior_walls", 0, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8

    def place(value):
        for _ in range(80):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = value
            return True
        return False

    if not place(2): return g
    sr, sc = next((r, c) for r in range(h) for c in range(w) if g[r][c] == 2)
    for _ in range(120):
        gr = rng.randint(1, h - 2); gc = rng.randint(1, w - 2)
        if g[gr][gc] != 0: continue
        if abs(gr - sr) + abs(gc - sc) < 4: continue
        g[gr][gc] = 3
        break
    for v, n in [(4, n_ka), (5, n_kb), (6, n_da), (7, n_db), (8, n_iw)]:
        for _ in range(n):
            place(v)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h): g[r][0] = 8; g[r][w - 1] = 8
    if name == "door_without_key":
        # Door 6 present but no key 4 — rule's unlock branch never
        # fires; path is blocked at the door.
        g[1][1] = 2
        g[6][9] = 3
        for r in range(2, 6): g[r][5] = 8
        g[3][5] = 6
        return g
    if name == "no_walls":
        # Only border walls — BFS reduces to Manhattan; rule's
        # interior-wall handling never fires.
        g[1][1] = 2
        g[6][9] = 3
        return g
    if name == "no_path":
        # Interior walls fully encircle goal — rule's "unreachable"
        # branch fires; output is empty.
        g[1][1] = 2
        g[4][5] = 3
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            g[4 + dr][5 + dc] = 8
        return g
    return g
