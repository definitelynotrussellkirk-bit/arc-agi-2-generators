"""Generator for arc_additional_puzzles_21_set13_bundle:E85.

Rule: for each cell (r,c), find first seed whose Manhattan distance ≤1;
output color is that seed's color, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seeds_too_close, seed_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cc74d7392ecd"
VERSION = "1.1.0"
TASK_ID = "cc74d7392ecd"
SUMMARY = "1-2 isolated non-bg seeds with empty cardinal neighbors."

INVARIANTS = [
    "1-2 non-bg seeds with no two within Manhattan distance 3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seeds_too_close", "seed_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "interior_isolated",
                       "valid": "interior_isolated"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    n = rng.randint(1, 2)
    placed = []
    for _ in range(40):
        if len(placed) >= n: break
        r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
        if all(abs(r - pr) + abs(c - pc) > 3 for pr, pc in placed):
            g[r][c] = rng.choice(palette)
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # empty grid → no neighborhoods to paint
        return g
    if name == "seeds_too_close":
        # 2 seeds within Manhattan 1 → neighborhoods overlap, first-match is order-dependent
        g[2][2] = 4
        g[2][3] = 6
        return g
    if name == "seed_at_edge":
        # seed in a corner → cardinal neighborhood is clipped to fewer cells
        g[0][0] = 5
        return g
    return g
