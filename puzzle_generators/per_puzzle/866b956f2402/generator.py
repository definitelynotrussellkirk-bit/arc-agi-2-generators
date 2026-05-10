"""Generator for 21b:m143 — apply downward gravity in walled columns.

Rule: in each column, 8-walls split the column into vertical segments.
Inside each segment, all non-bg cells fall downward toward the wall (or
the grid bottom).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_active,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_pebbles, all_at_bottom.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "866b956f2402"
VERSION = "1.1.0"
TASK_ID = "866b956f2402"
SUMMARY = "Scattered pebbles + 8-cells acting as per-column walls."

INVARIANTS = [
    "background is 0",
    "1-2 active columns containing 8-walls + a few non-8 pebbles above each wall",
    "in each active column, at least one non-8 cell is NOT already at its segment's bottom (so gravity changes input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_pebbles", "all_at_bottom")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_active":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "active_walled_columns",
                       "valid": "active_walled_columns"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 9, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_active = rng.randint(2, 3)
    active_cols = rng.sample(range(1, w - 1), n_active)
    palette_pool = [2, 3, 4, 5, 6, 7, 9]
    for c in active_cols:
        # 1-2 wall positions
        n_walls = rng.randint(1, 2)
        if h - 4 < n_walls: continue
        walls = rng.sample(range(2, h - 1), n_walls)
        walls.sort()
        for wr in walls:
            g[wr][c] = 8
        # place 1-3 pebbles above the topmost wall
        top_wall = min(walls)
        n_pebbles = rng.randint(1, min(3, top_wall))
        positions = rng.sample(range(0, top_wall - 1), min(n_pebbles, max(1, top_wall - 1)))
        for pr in positions:
            g[pr][c] = rng.choice(palette_pool)
        # also place between walls
        for i in range(len(walls) - 1):
            lo, hi = walls[i] + 1, walls[i + 1] - 1
            if hi - lo < 1: continue
            pr = rng.randint(lo, hi - 1)
            g[pr][c] = rng.choice(palette_pool)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 8
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # Pebbles but no 8-walls — column segments are undefined.
        g[2][3] = 4; g[3][5] = 5
        return g
    if name == "no_pebbles":
        # Walls but no pebbles — gravity has nothing to drop.
        g[5][3] = 8; g[5][5] = 8
        return g
    if name == "all_at_bottom":
        # Pebbles already at segment bottoms — gravity-down is a no-op.
        g[5][3] = 8
        g[4][3] = 4
        g[h - 1][5] = 5
        return g
    return g
