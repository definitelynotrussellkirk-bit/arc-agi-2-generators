"""Generator for arc_puzzle_bank_21_set24_bundle:easy_p07.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seed_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multiple_seeds_per_compartment.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9339b47bb5d5"
VERSION = "1.1.0"
TASK_ID = "9339b47bb5d5"
SUMMARY = "Seeds cast row and column crosshairs inside wall-bounded compartments."

INVARIANTS = [
    "background is 0",
    "wall color is 5",
    "each compartment contains at most one non-wall seed",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multiple_seeds_per_compartment")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "cross_walls_with_seeds",
                       "valid": "cross_walls_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        seed_count = ctx.draw_int("seed_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        seed_count = ctx.draw_int("seed_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        seed_count = ctx.draw_int("seed_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    wall_r = rng.randint(3, h - 4)
    wall_c = rng.randint(3, w - 4)
    for c in range(w):
        grid[wall_r][c] = 5
    for r in range(h):
        grid[r][wall_c] = 5
    compartments = [
        (0, wall_r - 1, 0, wall_c - 1),
        (0, wall_r - 1, wall_c + 1, w - 1),
        (wall_r + 1, h - 1, 0, wall_c - 1),
        (wall_r + 1, h - 1, wall_c + 1, w - 1),
    ]
    rng.shuffle(compartments)
    colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], min(seed_count, 8))
    for index, (r0, r1, c0, c1) in enumerate(compartments[:seed_count]):
        r = rng.randint(r0, r1)
        c = rng.randint(c0, c1)
        grid[r][c] = colors[index % len(colors)]
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # seeds without crosshair walls → no compartment boundaries to bound rays within
        g[1][1] = 4
        g[3][5] = 6
        g[6][7] = 7
        return g
    if name == "no_seeds":
        # walls alone, no seeds → no rays to cast
        for c in range(w):
            g[4][c] = 5
        for r in range(h):
            g[r][5] = 5
        return g
    if name == "multiple_seeds_per_compartment":
        # 2 seeds in one compartment → "at most one seed" precondition fails
        for c in range(w):
            g[4][c] = 5
        for r in range(h):
            g[r][5] = 5
        g[1][1] = 4
        g[2][2] = 6  # both in TL compartment
        g[7][8] = 7
        return g
    return g
