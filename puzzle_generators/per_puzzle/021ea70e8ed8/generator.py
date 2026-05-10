"""Generator for arc_puzzle_bank_twentieth21:E135 — vertical connect same-color pairs.

Rule: each non-empty column has exactly 2 cells of the same color. Output
draws a vertical line of that color between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, adjacent_pair, mixed_colors_in_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "021ea70e8ed8"
VERSION = "1.1.0"
TASK_ID = "021ea70e8ed8"
SUMMARY = "1-3 columns each have 2 cells of the same color at separated rows."

INVARIANTS = [
    "background is 0",
    "1-3 columns each have exactly 2 cells of the same color (separated by ≥2 rows)",
    "different columns use different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "adjacent_pair", "mixed_colors_in_col")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cols":         {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "separated_col_endpoints",
                       "valid": "separated_col_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..5"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 4, 5)
        n = ctx.draw_int("n_cols", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 5, 6)
        n = ctx.draw_int("n_cols", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 4, 6)
        n = ctx.draw_int("n_cols", 1, min(3, w))
    n = min(n, w)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for c, color in zip(cols, colors):
        r1 = rng.randint(0, h - 4)
        r2 = rng.randint(r1 + 2, h - 1)
        g[r1][c] = color
        g[r2][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 5
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only → no pair to connect, rule has nothing to do
        g[1][1] = 4
        g[3][3] = 6
        return g
    if name == "adjacent_pair":
        # endpoints adjacent (distance 1) → no cells "between" them
        g[2][1] = 4; g[3][1] = 4   # adjacent
        g[1][3] = 6; g[2][3] = 6   # adjacent
        return g
    if name == "mixed_colors_in_col":
        # column has 2 cells but DIFFERENT colors → "same-color pair" precondition fails
        g[1][1] = 4; g[5][1] = 6   # different colors in same col
        g[2][3] = 3; g[6][3] = 7   # different colors in same col
        return g
    return g
