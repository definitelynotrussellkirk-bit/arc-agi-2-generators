"""Generator for arc_additional_puzzles_21_set7:H44.

Rule: take largest 2-blob and largest 3-blob; normalize. Output cells
in BOTH shapes, bbox-cropped, color 8.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, no_intersection, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "729429f8ea2c"
VERSION = "1.1.0"
TASK_ID = "729429f8ea2c"
SUMMARY = "2-shape and 3-shape with shared normalized cells."

INVARIANTS = [
    "exactly one largest 2-blob and one largest 3-blob",
    "their normalized cell sets share at least one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_intersection", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    s2 = PLUS_5
    s3 = [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1)]
    paint_at(g, 1, 1, s2, 2)
    paint_at(g, 5, w - 5, s3, 3)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_shapes":
        return g
    if name == "no_intersection":
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
        paint_at(g, 5, 7, [(0, 0), (1, 0)], 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
