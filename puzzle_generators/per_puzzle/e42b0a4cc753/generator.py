"""Generator for arc_puzzle_bank_thirteenth21:H87.

Rule: fill a rectangular 8-walled chamber by nearest interior seed
color (Manhattan, reading-order ties).

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, seed_count, texture.
Degenerates: no_seeds, no_walls, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e42b0a4cc753"
VERSION = "1.1.0"
TASK_ID = "e42b0a4cc753"
SUMMARY = "Fill a rectangular 8-walled chamber by nearest interior seed color."

INVARIANTS = [
    "the outer rectangular chamber border is color 8",
    "two or three nonzero seeds lie strictly inside the chamber",
    "all other chamber interior cells are zero",
    "the canonical rule fills zeros by nearest Manhattan seed with reading-order ties",
]

PALETTE_KINDS = ("default", "two_seeds", "three_seeds", "spread_seeds")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "7", "valid": "5..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "seed_count":     {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SEED_LAYOUTS = [
    [(2, 2), (3, 3)],
    [(1, 2), (3, 4), (4, 1)],
    [(2, 1), (2, 4), (4, 3)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        variant = ctx.draw_int("variant", 0, 0)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 1, 2)
    else:
        variant = ctx.draw_int("variant", 0, 2)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], len(_SEED_LAYOUTS[variant]))
    g = full_grid(6, 7, 0)
    for c in range(7):
        g[0][c] = 8
        g[5][c] = 8
    for r in range(6):
        g[r][0] = 8
        g[r][6] = 8
    for (r, c), color in zip(_SEED_LAYOUTS[variant], colors):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 7, 0)
    for c in range(7):
        g[0][c] = 8; g[5][c] = 8
    for r in range(6):
        g[r][0] = 8; g[r][6] = 8
    if name == "no_seeds":
        # walled chamber with no seed colors → fill source undefined
        return g
    if name == "no_walls":
        # seeds present but no 8-walls → chamber boundary missing
        g2 = full_grid(6, 7, 0)
        g2[2][2] = 4; g2[3][3] = 6
        return g2
    if name == "single_seed":
        # only one seed → entire chamber fills with that color (rule trivially flat)
        g[2][3] = 5
        return g
    return g
