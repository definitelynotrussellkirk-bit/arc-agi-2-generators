"""Generator for arc_puzzle_bank_21_set9_s:S9_M2.

Rule: 9-walled rect-frame contains a single seed. Cells inside the
room at odd BFS-distance from seed (through 0-cells, blocked by 9s)
get color 8. Seed stays. Walls stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_walls, multiple_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "94258b3b6105"
VERSION = "1.1.0"
TASK_ID = "94258b3b6105"
SUMMARY = "9-walled room with one seed cell inside (color 2)."

INVARIANTS = [
    "background is 0",
    "exactly one closed 9-rect-outline frame",
    "exactly one seed (color 2) inside the room interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_walls", "multiple_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "1", "valid": "1"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "interior_seed",
                       "valid": "interior_seed"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1, c1 = 1, 1
    r2, c2 = h - 2, w - 2
    for c in range(c1, c2 + 1):
        g[r1][c] = 9; g[r2][c] = 9
    for r in range(r1, r2 + 1):
        g[r][c1] = 9; g[r][c2] = 9
    sr = rng.randint(r1 + 1, r2 - 1)
    sc = rng.randint(c1 + 1, c2 - 1)
    g[sr][sc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    r1, c1 = 1, 1
    r2, c2 = h - 2, w - 2
    if name == "no_seed":
        # walls present but no seed → BFS source undefined, no odd-distance cells
        for c in range(c1, c2 + 1):
            g[r1][c] = 9; g[r2][c] = 9
        for r in range(r1, r2 + 1):
            g[r][c1] = 9; g[r][c2] = 9
        return g
    if name == "no_walls":
        # seed without surrounding walls → BFS escapes the room, parity meaningless
        g[h // 2][w // 2] = 2
        return g
    if name == "multiple_seeds":
        # two seeds in the room → odd-distance is computed from each, results conflict
        for c in range(c1, c2 + 1):
            g[r1][c] = 9; g[r2][c] = 9
        for r in range(r1, r2 + 1):
            g[r][c1] = 9; g[r][c2] = 9
        g[3][3] = 2
        g[5][5] = 2
        return g
    return g
