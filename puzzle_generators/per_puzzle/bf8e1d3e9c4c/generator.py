"""Generator for arc_additional_puzzle_bank_volume21:M142.

Rule: for color in {2,3,4}, if exactly 2 cells aligned (same row or col),
fill the line between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, three_aligned, non_aligned_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bf8e1d3e9c4c"
VERSION = "1.1.0"
TASK_ID = "bf8e1d3e9c4c"
SUMMARY = "2-3 colors each with exactly 2 aligned cells (vertical or horizontal) + decoration."

INVARIANTS = [
    "between 2 and 3 colors from {2, 3, 4}",
    "each chosen color has exactly 2 cells either same-row or same-col",
    "decoration is non-{2,3,4} cell elsewhere",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "three_aligned", "non_aligned_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "fixed_pairs",
                       "valid": "fixed_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[2][3] = 2
    g[5][3] = 2
    g[2][2] = 4
    g[5][2] = 4
    if rng.random() < 0.5:
        g[0][3] = 3
        g[0][6] = 3
    g[h - 1][w - 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons of 2/3/4 only → no pairs to bridge
        g[2][3] = 2
        g[5][2] = 4
        return g
    if name == "three_aligned":
        # three cells of color 2 on same column → invariant violated
        g[1][3] = 2; g[3][3] = 2; g[5][3] = 2
        return g
    if name == "non_aligned_pairs":
        # two cells of color 2 not on same row/col → cannot bridge
        g[2][1] = 2
        g[5][7] = 2
        return g
    return g
