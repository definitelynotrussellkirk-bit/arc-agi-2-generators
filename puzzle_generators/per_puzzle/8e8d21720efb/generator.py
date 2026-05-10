"""Generator for arc_additional_puzzles_21_set7:E47 — Keep only non-bg cells with same-color cardinal neighbor.

Rule: each non-bg cell with at least one cardinal neighbor of the
same color is kept; isolated singletons are erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, all_blobs, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "8e8d21720efb"
VERSION = "1.1.0"
TASK_ID = "8e8d21720efb"
SUMMARY = "Mix of multi-cell blobs and isolated singletons in distinct colors."

INVARIANTS = [
    "≥2 multi-cell blobs (cardinal-connected, ≥2 cells)",
    "≥2 isolated singletons (will get erased)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "all_blobs", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "blobs_with_singleton_decoys",
                       "valid": "blobs_with_singleton_decoys"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 4)
    pair = [(0, 0), (0, 1)]
    L = [(0, 0), (0, 1), (1, 1)]
    paint_at(g, rng.randint(0, 1), rng.randint(0, 2), pair, pal[0])
    paint_at(g, rng.randint(h - 4, h - 3), rng.randint(w - 4, w - 3), L, pal[1])
    g[rng.randint(2, 4)][rng.randint(5, w - 3)] = pal[2]
    g[rng.randint(h - 3, h - 2)][rng.randint(0, 2)] = pal[3]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # all cells are singletons → rule erases everything (output blank)
        g[1][1] = 4
        g[3][5] = 6
        g[5][2] = 3
        g[6][7] = 7
        return g
    if name == "all_blobs":
        # all cells are in multi-cell blobs → rule keeps everything (input == output)
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 4, 4, [(0, 0), (0, 1), (1, 1)], 6)
        return g
    if name == "no_cells":
        # blank → no input cells, rule has nothing to filter
        return g
    return g
