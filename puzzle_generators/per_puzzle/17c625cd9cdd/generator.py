"""Generator for 4b:m23 — connect aligned pairs.

Rule: each color appearing exactly twice on the same row/col → fill
the span between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, diagonal_only, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "17c625cd9cdd"
VERSION = "1.1.0"
TASK_ID = "17c625cd9cdd"
SUMMARY = "2-3 colors each twice, sharing a row OR a column."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears exactly twice on the same row OR same column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "diagonal_only", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "aligned_pairs",
                       "valid": "aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(0, h - 1)
                c1 = rng.randint(0, w - 4)
                c2 = rng.randint(c1 + 3, w - 1)
                if g[r][c1] == 0 and g[r][c2] == 0:
                    g[r][c1] = color; g[r][c2] = color; break
            else:
                c = rng.randint(0, w - 1)
                r1 = rng.randint(0, h - 4)
                r2 = rng.randint(r1 + 3, h - 1)
                if g[r1][c] == 0 and g[r2][c] == 0:
                    g[r1][c] = color; g[r2][c] = color; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # only singletons → no pairs to connect
        g[2][3] = 4
        g[4][7] = 6
        return g
    if name == "diagonal_only":
        # 2 cells of same color on diagonal → "row/col aligned" precondition fails
        g[1][1] = 4; g[3][3] = 4
        g[5][8] = 6; g[6][7] = 6
        return g
    if name == "adjacent_pair":
        # pair separated by 1 → segment between them is empty (length-0)
        g[2][3] = 4; g[2][4] = 4
        g[5][7] = 6; g[5][8] = 6
        return g
    return g
