"""Generator for arc_additional_puzzle_bank_volume13:E91.

Rule: equal-colored aligned marker pairs are connected by same-color
segments.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, pairs_adjacent, multiple_pairs_same_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "80bd3177b03c"
VERSION = "1.1.0"
TASK_ID = "80bd3177b03c"
SUMMARY = "Equal-colored aligned marker pairs are connected by same-color segments."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "paired markers are aligned with a clear path between them",
    "all pairs use distinct rows to avoid path collisions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "pairs_adjacent", "multiple_pairs_same_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "horizontal_row_pairs",
                       "valid": "horizontal_row_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_pairs = ctx.draw_int("n_pairs", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_pairs = ctx.draw_int("n_pairs", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    colors = list(range(1, 10))
    rng.shuffle(colors)
    rows = rng.sample(range(h), min(n_pairs, h, len(colors)))
    for color, r in zip(colors, rows):
        c1 = rng.randint(0, w - 4)
        c2 = rng.randint(c1 + 2, w - 1)
        g[r][c1] = color
        g[r][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only → no pair connections
        g[2][3] = 4
        g[5][7] = 6
        return g
    if name == "pairs_adjacent":
        # markers touching → no gap to bridge
        g[2][3] = 4; g[2][4] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "multiple_pairs_same_row":
        # two pairs share a row → segments would collide, rule's path invariant breaks
        g[3][1] = 4; g[3][3] = 4
        g[3][5] = 6; g[3][7] = 6
        return g
    return g
