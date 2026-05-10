"""Generator for 16b:m108 — apply gravity inside vertical chambers.

Rule: vertical full-height 8-walls divide the grid into chambers.
Inside each chamber, all non-zero non-wall cells fall to the bottom row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_pebbles, all_in_bottom_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9ada70e7181"
VERSION = "1.1.0"
TASK_ID = "b9ada70e7181"
SUMMARY = "2-3 full-height 8-walls + scattered colored pebbles inside each chamber."

INVARIANTS = [
    "background is 0",
    "2-3 full-height columns of 8s split the grid into chambers",
    "each chamber has 1-3 scattered non-bg cells (none color 8)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_pebbles", "all_in_bottom_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "vertical_chambers",
                       "valid": "vertical_chambers"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_walls = rng.randint(2, 3)
    walls = rng.sample(range(2, w - 2), n_walls)
    walls.sort()
    for c in walls:
        for r in range(h):
            g[r][c] = 8
    edges = [-1] + walls + [w]
    palette_pool = [1, 2, 3, 4, 5, 6, 7, 9]
    for i in range(len(edges) - 1):
        c_lo, c_hi = edges[i] + 1, edges[i + 1] - 1
        if c_hi < c_lo: continue
        n_pebbles = rng.randint(1, min(3, (c_hi - c_lo + 1) * (h - 1)))
        placed = 0
        attempts = 0
        while placed < n_pebbles and attempts < 30:
            attempts += 1
            r = rng.randint(0, h - 2)
            c = rng.randint(c_lo, c_hi)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice(palette_pool)
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # Pebbles but no 8-walls — chambers are undefined, gravity has
        # no per-chamber boundary to respect.
        g[2][3] = 4; g[3][7] = 6; g[1][9] = 7
        return g
    if name == "no_pebbles":
        # 8-walls but no pebbles in any chamber — rule has nothing
        # to drop.
        for r in range(h): g[r][3] = 8; g[r][7] = 8
        return g
    if name == "all_in_bottom_row":
        # Walls + pebbles already on the bottom row — gravity is a
        # no-op, rule's effect is invisible.
        for r in range(h): g[r][3] = 8; g[r][7] = 8
        g[h - 1][1] = 4; g[h - 1][5] = 6; g[h - 1][9] = 7
        return g
    return g
