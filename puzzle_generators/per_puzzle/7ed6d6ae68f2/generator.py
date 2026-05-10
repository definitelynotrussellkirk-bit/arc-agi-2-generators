"""Generator for arc_additional_puzzle_bank_volume7:H44 — red/green compete through maze.

Rule: red and green seeds compete through a gray-wall maze; equal
distances stay blank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, maze_layout,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, sealed_chambers, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7ed6d6ae68f2"
VERSION = "1.1.0"
TASK_ID = "7ed6d6ae68f2"
SUMMARY = "Red and green seeds compete through a gray-wall maze; equal distances stay blank."

INVARIANTS = [
    "background is 0",
    "border and divider walls are 5",
    "there is exactly one red seed and one green seed",
    "at least one blank cell is reachable from each seed",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "sealed_chambers", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "maze_layout":    {"type": "str", "default": "split_with_gap",
                       "valid": "split_with_gap"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_walls_with_split",
                       "valid": "border_walls_with_split"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 11, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    split = rng.randint(4, w - 5)
    gap = rng.randint(2, h - 3)
    for r in range(1, h - 1):
        if r != gap:
            g[r][split] = 5
    if rng.choice([True, False]):
        for c in range(1, split):
            if c != split // 2:
                g[h // 2][c] = 5
    g[1 + rng.randint(0, max(0, gap - 2))][2] = 2
    g[h - 2 - rng.randint(0, max(0, h - gap - 3))][w - 3] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    # build full border + split for all variants
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    if name == "no_seeds":
        # walls but no red/green seeds → no competitors to flood from
        for r in range(1, h - 1):
            if r != 4: g[r][6] = 5
        return g
    if name == "sealed_chambers":
        # split with NO gap → seeds can never reach the other side
        for r in range(1, h - 1):
            g[r][6] = 5
        g[3][2] = 2
        g[7][w - 3] = 3
        return g
    if name == "single_seed":
        # only one seed → no competition / no equidistant cells possible
        for r in range(1, h - 1):
            if r != 4: g[r][6] = 5
        g[3][2] = 2
        return g
    return g
