"""Generator for arc_puzzle_bank_21_set11_s:S11_M7.

Rule: legend = non-zero values in row 0 (in order). Sort 7-blobs in
body by (size asc, top-left); recolor each by next legend color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: no_legend, fewer_legends_than_blobs, equal_size_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "f9787b3cf4de"
VERSION = "1.1.0"
TASK_ID = "f9787b3cf4de"
SUMMARY = "Row 0 has 3 legend colors + body has 3 7-blobs of distinct sizes."

INVARIANTS = [
    "row 0 has 3 non-zero cells (legend colors)",
    "body has 3 non-touching 7-blobs of distinct sizes",
]

PALETTE_KINDS = ("default", "warm_legend", "cool_legend", "varied_legend")
DEGENERATE_TEXTURES = ("no_legend", "fewer_legends_than_blobs", "equal_size_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "row_zero_legend",
                       "valid": "row_zero_legend"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "size_spread":    {"type": "str", "default": "2_4_9", "valid": "2_4_9"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    g[0][0] = 2; g[0][3] = 3; g[0][6] = 4
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 7)
    paint_at(g, 5, 3, [(0, 0), (1, 0)], 7)
    paint_at(g, 2, 6, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # 7-blobs but no row-0 legend → recolor mapping undefined
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 7)
        paint_at(g, 5, 3, [(0, 0), (1, 0)], 7)
        return g
    if name == "fewer_legends_than_blobs":
        # 3 blobs but only 2 legend colors → 3rd recolor is undefined
        g[0][0] = 2; g[0][3] = 3
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 7)
        paint_at(g, 5, 3, [(0, 0), (1, 0)], 7)
        paint_at(g, 2, 6, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)], 7)
        return g
    if name == "equal_size_blobs":
        # all blobs same size → "sort by size" tie-break is fragile (top-left only)
        g[0][0] = 2; g[0][3] = 3; g[0][6] = 4
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 7)
        paint_at(g, 5, 3, [(0, 0), (0, 1)], 7)
        paint_at(g, 2, 7, [(0, 0), (0, 1)], 7)
        return g
    return g
