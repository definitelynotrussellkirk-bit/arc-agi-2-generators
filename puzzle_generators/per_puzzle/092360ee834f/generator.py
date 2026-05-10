"""Generator for arc_puzzle_bank_21_set10_s:S10_M4.

Rule: the number of 1s in row 0 selects a color-3 body object by size;
selected cells become 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_size,
palette_size, position_bias, n_distinct_colors, header_kind, texture.
Degenerates: no_header, no_match, multiple_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "092360ee834f"
VERSION = "1.1.0"
TASK_ID = "092360ee834f"
SUMMARY = "The number of 1s in row 0 selects a color-3 body object by size; selected cells become 8."

INVARIANTS = [
    "row 0 contains a small count of color-1 cells",
    "one body color-3 object has exactly that many cells",
]

PALETTE_KINDS = ("default", "small_target", "medium_target", "large_target")
DEGENERATE_TEXTURES = ("no_header", "no_match", "multiple_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_size":    {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "header_then_body",
                       "valid": "header_then_body"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "header_kind":    {"type": "str", "default": "row_zero", "valid": "row_zero"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        k = ctx.draw_int("target_size", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        k = ctx.draw_int("target_size", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
        k = ctx.draw_int("target_size", 3, 5)
    g = full_grid(h, w, 0)
    for c in range(k):
        g[0][c] = 1
    target_cells = [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)][:k]
    paint_at(g, 2, 2, target_cells, 3)
    paint_at(g, h - 3, w - 4, [(0, 0), (0, 1)], 3)
    if k != 4:
        paint_at(g, h - 5, w - 3, [(0, 0), (1, 0), (1, 1), (2, 1)], 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_header":
        # body 3-objects but no row-0 1-header → which size to pick is undefined
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 3)
        paint_at(g, h - 3, w - 4, [(0, 0), (0, 1)], 3)
        return g
    if name == "no_match":
        # header says k=3 but no 3-object has exactly 3 cells
        for c in range(3):
            g[0][c] = 1
        paint_at(g, 2, 2, [(0, 0), (0, 1)], 3)
        paint_at(g, h - 3, w - 4, [(0, 0), (1, 0), (1, 1), (2, 1)], 3)
        return g
    if name == "multiple_match":
        # two 3-objects of size 3 → which one becomes 8 is ambiguous
        for c in range(3):
            g[0][c] = 1
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 3)
        paint_at(g, h - 3, w - 4, [(0, 0), (1, 0), (1, 1)], 3)
        return g
    return g
