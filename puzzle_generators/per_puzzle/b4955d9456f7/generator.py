"""Generator for arc_puzzle_bank_21_set10_s:S10_E6 — 2-cell same-color pairs at even row/col distance → midpoint = 8.

Rule: for each color appearing exactly twice, if cells are in same
row with even col-distance OR same col with even row-distance, set
the midpoint to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, alignment,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, odd_distance_pairs, diagonal_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b4955d9456f7"
VERSION = "1.1.0"
TASK_ID = "b4955d9456f7"
SUMMARY = "1-2 colors with exactly 2 cells aligned at even distance."

INVARIANTS = [
    "≥1 color with 2 cells aligned in same row or col, even distance ≥2",
    "1-2 distractor isolated cells of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "odd_distance_pairs", "diagonal_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "alignment":      {"type": "str", "default": "rng row|col|both", "valid": "row|col|both"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "even_distance_pairs",
                       "valid": "even_distance_pairs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 9], 3)
    r1 = rng.randint(0, h - 1)
    c1 = rng.randint(0, w - 5)
    distance = 2 * rng.randint(1, (w - c1 - 1) // 2)
    g[r1][c1] = pal[0]
    g[r1][c1 + distance] = pal[0]
    c2 = rng.randint(0, w - 1)
    r2 = rng.randint(0, h - 3)
    rdist = 2 * rng.randint(1, (h - r2 - 1) // 2)
    if g[r2][c2] == 0 and g[r2 + rdist][c2] == 0:
        g[r2][c2] = pal[1]
        g[r2 + rdist][c2] = pal[1]
    g[0][0] = pal[2] if g[0][0] == 0 else g[0][0]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # only singletons → no 2-cell pairs to find midpoints of
        g[2][3] = 4
        g[4][7] = 6
        return g
    if name == "odd_distance_pairs":
        # pairs aligned but odd distance → no integer midpoint, rule won't fire
        g[2][1] = 4; g[2][4] = 4  # distance 3 (odd)
        return g
    if name == "diagonal_pairs":
        # pairs on diagonal → "same row or col" precondition fails
        g[1][1] = 4; g[3][5] = 4
        g[5][8] = 6
        return g
    return g
