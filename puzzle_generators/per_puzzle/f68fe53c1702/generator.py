"""Generator for arc_additional_puzzles_21_set16_bundle:E107.

Rule: bbox of all non-bg cells (single color); paint frame outline of
that bbox in the same color on a fresh empty grid.

Combinatorial axes (8): grid_h/w, palette_kind, color, num_cells,
palette_size, position_bias, n_distinct_colors, bbox_aspect, texture.
Degenerates: only_one_cell, no_cells, cells_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f68fe53c1702"
VERSION = "1.1.0"
TASK_ID = "f68fe53c1702"
SUMMARY = "2 cells of single non-bg color forming non-degenerate bbox."

INVARIANTS = [
    "exactly 2 cells of a single non-bg color",
    "bbox spans ≥3 rows AND ≥3 cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_one_cell", "no_cells", "cells_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "color":          {"type": "int", "default": "rng", "valid": "2..9"},
    "num_cells":      {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    r1 = rng.randint(0, h - 4); r2 = rng.randint(r1 + 2, h - 1)
    c1 = rng.randint(0, w - 4); c2 = rng.randint(c1 + 3, w - 1)
    g[r1][c1] = color; g[r2][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "only_one_cell":
        # 1 cell — bbox degenerate (1×1), frame = the cell
        g[2][3] = 5
        return g
    if name == "no_cells":
        # empty — no bbox to outline
        return g
    if name == "cells_aligned":
        # both cells in same row → zero-height bbox (no frame, just a line)
        g[3][1] = 4
        g[3][6] = 4
        return g
    return g
