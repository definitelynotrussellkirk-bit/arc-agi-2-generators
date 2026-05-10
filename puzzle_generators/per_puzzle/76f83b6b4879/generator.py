"""Generator for arc_additional_puzzle_bank_volume21:H142.

Rule: red, green, and yellow seeds fill by wall-aware distance; ties
become cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, no_walls, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "76f83b6b4879"
VERSION = "1.1.0"
TASK_ID = "76f83b6b4879"
SUMMARY = "Red, green, and yellow seeds fill by wall-aware distance; ties become cyan."

INVARIANTS = [
    "background is 0",
    "gray cells block movement",
    "one seed of each color 2, 3, and 4 is present",
    "seed distances create both owned cells and cyan tie cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "walled_quadrants",
                       "valid": "walled_quadrants"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "walled", "valid": "walled"},
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
    c1 = w // 3
    c2 = (2 * w) // 3
    for r in range(1, h - 1):
        if r not in {h // 2, h // 2 + 1}:
            g[r][c1] = 5
        if r != h // 2:
            g[r][c2] = 5
    for c in range(1, w - 1):
        if c not in {c1 - 1, c1 + 1, c2 - 1, c2 + 1} and rng.choice([False, True, True]):
            g[h // 2][c] = 5
    g[1][w // 2] = 2
    g[h - 2][2] = 4
    g[h - 2][w - 3] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # walls but no seeds → nothing to flood-fill
        for r in range(1, h - 1):
            g[r][w // 2] = 5
        return g
    if name == "no_walls":
        # seeds without walls → wall-aware distance degenerates to plain Manhattan
        g[1][w // 2] = 2
        g[h - 2][2] = 4
        g[h - 2][w - 3] = 3
        return g
    if name == "single_seed":
        # only one seed → all cells go to that seed, no tie cells, no cyan
        c1 = w // 3
        for r in range(1, h - 1):
            if r not in {h // 2, h // 2 + 1}:
                g[r][c1] = 5
        g[1][w // 2] = 2
        return g
    return g
