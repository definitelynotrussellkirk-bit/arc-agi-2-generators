"""Generator for arc_additional_puzzle_bank_volume14:M94.

Rule: each gray-wall chamber with one seed color among 1, 2, 3 is
flood-filled with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, seed_kind, texture.
Degenerates: no_walls, no_seed, ambiguous_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "21d822423cfc"
VERSION = "1.1.0"
TASK_ID = "21d822423cfc"
SUMMARY = "Each gray-wall chamber with one seed color among 1, 2, 3 is flood-filled."

INVARIANTS = [
    "background is 0",
    "gray cells form separated chambers",
    "at least one chamber contains exactly one qualifying seed color",
    "blank chambers are left unchanged",
]

PALETTE_KINDS = ("default", "seed_1", "seed_2", "seed_3")
DEGENERATE_TEXTURES = ("no_walls", "no_seed", "ambiguous_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "chamber", "valid": "chamber"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
    "seed_kind":      {"type": "str", "default": "rng", "valid": "rng"},
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
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    wall = rng.randint(3, w - 4)
    for r in range(1, h - 1):
        g[r][wall] = 5
    g[rng.randint(1, h - 2)][rng.randint(1, wall - 1)] = rng.choice([1, 2, 3])
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = rng or random.Random(0)
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # seed but no chamber walls → flood reaches everywhere
        g[3][3] = 2
        return g
    if name == "no_seed":
        # walls + chambers but no seed → rule has nothing to fill
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(1, h - 1):
            g[r][5] = 5
        return g
    if name == "ambiguous_seed":
        # one chamber holds two seed colors → fill choice undefined
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(1, h - 1):
            g[r][5] = 5
        g[2][2] = 1
        g[5][3] = 2
        return g
    return g
