"""Generator for arc_additional_puzzle_bank_volume15:M104 — fill chamber by majority seed color.

Rule: gray walls partition the grid into chambers; the chamber with the
most seeds is filled using its majority seed color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_seed_counts, no_seeds, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6ecd8be24495"
VERSION = "1.1.0"
TASK_ID = "6ecd8be24495"
SUMMARY = "The chamber with the most seeds is filled using its majority seed color."

INVARIANTS = [
    "background is 0",
    "gray walls partition the grid into chambers",
    "one chamber has strictly more nonzero seeds than the others",
    "the selected chamber has a unique majority seed color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_seed_counts", "no_seeds", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "wall_split_with_majority_seeds",
                       "valid": "wall_split_with_majority_seeds"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 10, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    wall = rng.randint(4, w - 5)
    for r in range(1, h - 1):
        g[r][wall] = 5
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    other = 9 if color != 9 else 8
    seeds = [(1, 1, color), (2, 2, color), (h - 3, 2, other), (1, wall + 1, other)]
    for r, c, v in seeds:
        g[r][c] = v
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    for r in range(h): g[r][0] = 5; g[r][w - 1] = 5
    for c in range(w): g[0][c] = 5; g[h - 1][c] = 5
    wall = 6
    for r in range(1, h - 1): g[r][wall] = 5
    if name == "tied_seed_counts":
        # both chambers have same seed count → "max chamber" is ambiguous
        g[1][1] = 4; g[2][2] = 4    # left: 2 seeds
        g[1][7] = 6; g[2][8] = 6    # right: 2 seeds (tied)
        return g
    if name == "no_seeds":
        # walls present but no seeds → no chamber has seeds, rule has nothing to fill
        return g
    if name == "no_walls":
        # walls absent → grid not partitioned into chambers
        g2 = full_grid(h, w, 0)
        g2[2][3] = 4; g2[3][4] = 4
        g2[5][7] = 6
        return g2
    return g
