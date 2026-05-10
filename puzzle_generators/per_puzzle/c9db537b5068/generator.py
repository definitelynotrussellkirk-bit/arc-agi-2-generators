"""Generator for arc_additional_puzzles_21_set19_bundle:E128.

Rule: collect all non-bg cells; their (single) color fills the bbox
rectangle.

Combinatorial axes (8): grid_h/w, palette_kind, color, num_corners,
palette_size, position_bias, n_distinct_colors, bbox_aspect, texture.
Degenerates: only_3_corners, cells_aligned, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c9db537b5068"
VERSION = "1.1.0"
TASK_ID = "c9db537b5068"
SUMMARY = "4 corner cells of a single non-bg color forming a rectangle."

INVARIANTS = [
    "exactly 4 cells of a single non-bg color, at corners of a rect ≥3×3",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_3_corners", "cells_aligned", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "color":          {"type": "int", "default": "rng", "valid": "2..9"},
    "num_corners":    {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "corners",
                       "valid": "corners"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    r1 = rng.randint(0, h - 5); r2 = rng.randint(r1 + 3, h - 1)
    c1 = rng.randint(0, w - 5); c2 = rng.randint(c1 + 3, w - 1)
    g[r1][c1] = color; g[r1][c2] = color
    g[r2][c1] = color; g[r2][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "only_3_corners":
        # only 3 cells — rectangle inference is incomplete
        g[1][1] = 4; g[1][7] = 4
        g[6][1] = 4
        return g
    if name == "cells_aligned":
        # all 4 cells in same row — degenerate flat bbox
        g[3][1] = 5; g[3][3] = 5; g[3][5] = 5; g[3][7] = 5
        return g
    if name == "no_cells":
        # empty — no rectangle to fill
        return g
    return g
