"""Generator for arc_puzzle_bank_21_set5_e:easy_e01.

Rule: each non-gray seed casts its color rightward until a gray blocker
or the border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, no_blockers, blocker_left_of_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "26dbe76edccd"
VERSION = "1.1.0"
TASK_ID = "26dbe76edccd"
SUMMARY = "Each non-gray seed casts its color rightward until a gray blocker or the border."

INVARIANTS = [
    "background is 0",
    "gray 5 cells are blockers",
    "each active row has one colored seed",
    "seed rays travel horizontally to the right",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_blockers", "blocker_left_of_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seeds":          {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row_seeds_with_blockers",
                       "valid": "row_seeds_with_blockers"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n = min(ctx.draw_int("seeds", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        n = min(ctx.draw_int("seeds", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 11)
        n = min(ctx.draw_int("seeds", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n)
    for r, color in zip(rng.sample(range(h), n), colors):
        c = rng.randint(0, w - 3)
        g[r][c] = color
        if rng.random() < 0.65 and c + 2 < w:
            g[r][rng.randint(c + 2, w - 1)] = 5
    for _ in range(rng.randint(1, 3)):
        rr = rng.randrange(h)
        cc = rng.randrange(w)
        if g[rr][cc] == 0:
            g[rr][cc] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # only blockers, no seeds → no rays to cast
        g[2][3] = 5; g[4][6] = 5
        return g
    if name == "no_blockers":
        # seeds without blockers → rays travel to right border
        g[2][1] = 4
        g[5][2] = 6
        return g
    if name == "blocker_left_of_seed":
        # blocker on left of seed → rightward ray ignores it (rule unaffected)
        g[2][1] = 5; g[2][3] = 4
        g[5][2] = 5; g[5][6] = 6
        return g
    return g
