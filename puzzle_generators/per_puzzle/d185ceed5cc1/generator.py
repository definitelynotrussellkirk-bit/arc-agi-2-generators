"""Generator for 20b:m136 — apply rightward gravity in each walled segment.

Rule: full-height 8-walls + outer 8-frame divide rows into chambers.
Inside each chamber, all non-bg cells slide rightward to the wall.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_pebbles, all_at_right.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d185ceed5cc1"
VERSION = "1.1.0"
TASK_ID = "d185ceed5cc1"
SUMMARY = "Full-height 8-walls (left/right edges + 1 internal) + scattered pebbles in chambers."

INVARIANTS = [
    "background is 0",
    "leftmost and rightmost columns are full 8",
    "exactly one full-height internal 8-column",
    "each chamber has 2-4 scattered non-bg pebbles, none in the column adjacent to the right wall (else input==output)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_pebbles", "all_at_right")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "1", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "frame_with_internal_walls",
                       "valid": "frame_with_internal_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    # full-height left/right walls
    for r in range(h):
        g[r][0] = 8; g[r][w - 1] = 8
    # one internal wall
    mid = rng.randint(3, w - 4)
    for r in range(h):
        g[r][mid] = 8
    palette = [1, 2, 3, 4, 5, 6, 7, 9]
    edges = [0, mid, w - 1]
    for i in range(len(edges) - 1):
        c_lo, c_hi = edges[i] + 1, edges[i + 1] - 2  # leave column adjacent to right wall empty
        if c_hi < c_lo: continue
        n = rng.randint(2, 4)
        placed = 0; attempts = 0
        while placed < n and attempts < 30:
            attempts += 1
            r = rng.randint(0, h - 1)
            c = rng.randint(c_lo, c_hi)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice(palette); placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 11
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # Pebbles but no walls — chambers are undefined.
        g[2][3] = 4; g[3][7] = 5
        return g
    if name == "no_pebbles":
        # Walls but no pebbles — gravity has nothing to slide.
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        for r in range(h): g[r][5] = 8
        return g
    if name == "all_at_right":
        # All pebbles already adjacent to right wall — gravity is a no-op.
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
        for r in range(h): g[r][5] = 8
        g[1][4] = 4; g[2][9] = 5
        return g
    return g
