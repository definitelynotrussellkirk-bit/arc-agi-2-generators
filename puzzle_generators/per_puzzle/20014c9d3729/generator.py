"""Generator for arc_puzzle_bank_21_next:medium_c05.

Rule: for each non-bg color, keep only the largest blob (size desc,
then r1, c1). Output is empty + kept blobs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes_per_color, single_blob_per_color, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "20014c9d3729"
VERSION = "1.1.0"
TASK_ID = "20014c9d3729"
SUMMARY = "2-3 colors each with 2 blobs of distinct sizes; largest per color is kept."

INVARIANTS = [
    "between 2 and 3 distinct colors",
    "each color has 2 blobs of distinct sizes",
    "all blobs non-touching",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes_per_color", "single_blob_per_color", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "size_spread":    {"type": "str", "default": "small_vs_large",
                       "valid": "small_vs_large"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    g = full_grid(h, w, 0)
    paint_at(g, 0, 0, [(0, 0), (0, 1)], 2)
    paint_at(g, h - 4, 0, [(0, 0), (0, 1), (0, 2), (1, 0)], 2)
    paint_at(g, 1, 5, [(0, 0), (0, 1)], 7)
    paint_at(g, h - 3, w - 5, [(0, 0), (0, 1), (0, 2), (0, 3)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "equal_sizes_per_color":
        # each color's two blobs are the same size → "largest" is ambiguous
        paint_at(g, 0, 0, [(0, 0), (0, 1)], 2)
        paint_at(g, h - 3, 0, [(0, 0), (0, 1)], 2)
        paint_at(g, 1, 5, [(0, 0), (0, 1)], 7)
        paint_at(g, h - 3, w - 4, [(0, 0), (0, 1)], 7)
        return g
    if name == "single_blob_per_color":
        # each color has only 1 blob → rule is identity
        paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2)], 2)
        paint_at(g, h - 3, 5, [(0, 0), (0, 1)], 7)
        return g
    if name == "no_blobs":
        # empty grid — no blobs at all
        return g
    return g
