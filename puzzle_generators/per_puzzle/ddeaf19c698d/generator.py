"""Generator for arc_puzzle_bank_21_set16_bundle:easy_p02.

Rule: singleton seeds expand into a horizontal three-cell brush
clipped at edges.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seed_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seeds_at_edge, seeds_overlap_brushes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ddeaf19c698d"
VERSION = "1.1.0"
TASK_ID = "ddeaf19c698d"
SUMMARY = "Separated singleton seeds for horizontal brush expansion."

INVARIANTS = [
    "background is 0",
    "all nonzero cells are singleton seeds",
    "seed brush neighborhoods do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seeds_at_edge", "seeds_overlap_brushes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_count":     {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_singletons",
                       "valid": "spaced_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        seed_count = ctx.draw_int("seed_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        seed_count = ctx.draw_int("seed_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
        seed_count = ctx.draw_int("seed_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=seed_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            r = rng.randrange(h)
            c = rng.randrange(w)
            brush = {(r, cc) for cc in range(max(0, c - 1), min(w, c + 2))}
            if not (brush & occupied):
                g[r][c] = color
                occupied |= brush
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank grid → no seeds to expand, rule is identity
        return g
    if name == "seeds_at_edge":
        # seeds on the leftmost/rightmost column → brush is clipped, only 2 cells painted
        g[2][0] = 4; g[4][0] = 6
        g[3][w - 1] = 3; g[5][w - 1] = 8
        return g
    if name == "seeds_overlap_brushes":
        # seeds within 2 cells in same row → brushes overlap, conflicting paints
        g[2][2] = 4; g[2][3] = 6   # adjacent seeds, brushes (1..3) and (2..4) overlap
        g[5][5] = 3; g[5][6] = 8
        return g
    return g
