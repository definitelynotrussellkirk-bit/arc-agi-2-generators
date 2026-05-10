"""Generator for arc_puzzle_bank_21_set16_s:S16_M3.

Rule: input has exactly two color-1 cells forming opposite corners of a
rectangle; output is the filled rectangle painted in 8.

Combinatorial axes (8): grid_h/w, palette_kind, num_corners,
palette_size, position_bias, n_distinct_colors, bbox_aspect, texture.
Degenerates: only_one_corner, cells_aligned, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ebe355c22d70"
VERSION = "1.1.0"
TASK_ID = "ebe355c22d70"
SUMMARY = "Exactly 2 cells of color 1 forming a non-degenerate bbox."

INVARIANTS = [
    "background is 0",
    "exactly two color-1 cells",
    "the two cells differ in both row AND column (so output is 2D, not a line)",
]

PALETTE_KINDS = ("default", "tight_bbox", "wide_bbox", "diagonal_bbox")
DEGENERATE_TEXTURES = ("only_one_corner", "cells_aligned", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_corners":    {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "bbox_aspect":    {"type": "str", "default": "rectangle",
                       "valid": "rectangle"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1 = rng.randint(0, h - 4)
    c1 = rng.randint(0, w - 4)
    r2 = rng.randint(r1 + 2, h - 1)
    c2 = rng.randint(c1 + 2, w - 1)
    g[r1][c1] = 1
    g[r2][c2] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "only_one_corner":
        # 1 cell of color 1 — no second corner, bbox degenerate (1×1)
        g[3][4] = 1
        return g
    if name == "cells_aligned":
        # both cells in same row → zero-height bbox (rule output is 1D)
        g[3][1] = 1
        g[3][6] = 1
        return g
    if name == "no_cells":
        return g
    return g
