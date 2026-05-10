"""Generator for v0_original:easy_05.

Rule: each non-zero seed cell paints a down-right diagonal of its
color until the grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seed_at_bottom_right, two_seeds_same_diag.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f20defd6ea3c"
VERSION = "1.1.0"
TASK_ID = "f20defd6ea3c"
SUMMARY = "1-3 non-zero seed cells (any color) at distinct positions."

INVARIANTS = [
    "background is 0",
    "1-3 single-cell seeds in distinct non-zero colors at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seed_at_bottom_right", "two_seeds_same_diag")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 5, 6)
        n = ctx.draw_int("n_seeds", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_seeds", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 5, 7)
        n = ctx.draw_int("n_seeds", 1, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in colors:
        for _t in range(40):
            r = rng.randint(0, h - 2); c = rng.randint(0, w - 2)
            if g[r][c] != 0: continue
            g[r][c] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 6
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # empty grid — no diagonals to paint
        return g
    if name == "seed_at_bottom_right":
        # seed at (h-1, w-1) → diagonal length is 1 (just the seed)
        g[h - 1][w - 1] = 5
        return g
    if name == "two_seeds_same_diag":
        # two seeds on the same down-right diagonal → second seed sits inside first ray
        g[1][1] = 4
        g[3][3] = 6
        return g
    return g
