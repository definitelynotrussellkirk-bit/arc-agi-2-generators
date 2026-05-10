"""Generator for arc_additional_puzzles_21_set22_bundle:E153.

Rule: take all non-bg cells (single color); compute bbox; output draws
2 diagonals of that color: top-left to bottom-right, and top-right
to bottom-left, of bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, bbox_side,
palette_size, position_bias, n_distinct_colors, rect_aspect, texture.
Degenerates: no_cells, single_cell, non_square_bbox.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6ebcd82f8e83"
VERSION = "1.1.0"
TASK_ID = "6ebcd82f8e83"
SUMMARY = "2 cells of a single non-bg color at top corners of a square bbox."

INVARIANTS = [
    "exactly 2 cells of a single non-bg color",
    "bbox is square (r2-r1 == c2-c1)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "single_cell", "non_square_bbox")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bbox_side":      {"type": "int", "default": "rng 2..min(h,w)-3",
                       "valid": "2..9"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "diag_corners", "valid": "diag_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "rect_aspect":    {"type": "str", "default": "square", "valid": "square"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    side = rng.randint(2, min(h, w) - 3)
    r1 = rng.randint(0, h - side - 1); c1 = rng.randint(0, w - side - 1)
    g[r1][c1] = color
    g[r1 + side][c1 + side] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid — no bbox, no diagonals
        return g
    if name == "single_cell":
        # only 1 cell → bbox is degenerate (1×1), diagonals collapse
        g[3][4] = 5
        return g
    if name == "non_square_bbox":
        # 2 cells with non-square bbox → "square bbox" predicate fails; X uneven
        g[1][1] = 4
        g[3][6] = 4
        return g
    return g
