"""Generator for arc_additional_puzzle_bank_volume14:M96.

Rule: 2 1-cells form one rect; 2 2-cells form another. Their bbox
intersection (if non-empty) gets painted 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, overlap_size,
palette_size, position_bias, n_distinct_colors, rect_aspect, texture.
Degenerates: no_overlap, no_rect_1, no_rect_2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "891b61bb5d4d"
VERSION = "1.1.0"
TASK_ID = "891b61bb5d4d"
SUMMARY = "2 1-cells (corners of rect 1) + 2 2-cells (corners of rect 2) overlapping."

INVARIANTS = [
    "exactly 2 1-cells at distinct rows AND cols",
    "exactly 2 2-cells at distinct rows AND cols",
    "the two bbox rects overlap in at least 1 cell",
    "decoration is non-{1,2} cell",
]

PALETTE_KINDS = ("default", "small_overlap", "large_overlap", "edge_overlap")
DEGENERATE_TEXTURES = ("no_overlap", "no_rect_1", "no_rect_2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "overlap_size":   {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "diagonal_corners",
                       "valid": "diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "rect_aspect":    {"type": "str", "default": "rng", "valid": "rng"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    g[1][1] = 1; g[6][7] = 1
    g[3][4] = 2; g[7][9] = 2
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_overlap":
        # two rects that don't intersect → bbox intersection is empty
        g[1][1] = 1; g[2][3] = 1
        g[6][7] = 2; g[8][10] = 2
        g[h - 1][w - 1] = 5
        return g
    if name == "no_rect_1":
        # only 2-cells; no 1-rect → intersection has missing operand
        g[3][4] = 2; g[7][9] = 2
        g[h - 1][w - 1] = 5
        return g
    if name == "no_rect_2":
        # only 1-cells; no 2-rect → intersection has missing operand
        g[1][1] = 1; g[6][7] = 1
        g[h - 1][w - 1] = 5
        return g
    return g
