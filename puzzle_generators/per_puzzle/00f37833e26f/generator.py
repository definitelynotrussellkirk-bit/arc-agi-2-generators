"""Generator for arc_additional_puzzles_21_set6:H41.

Rule: normalize 3-shape and 5-shape; output cells in 3-shape but not in
5-shape, bbox-cropped, color 3.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, no_subset, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "00f37833e26f"
VERSION = "1.1.0"
TASK_ID = "00f37833e26f"
SUMMARY = "3-shape (larger) and 5-shape (subset of 3) placed apart."

INVARIANTS = [
    "exactly one 3-blob and one 5-blob",
    "normalized 5-cells are a strict subset of normalized 3-cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_subset", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
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
    s3 = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    s5 = [(0, 0), (1, 0), (1, 2)]
    paint_at(g, 1, 1, s3, 3)
    paint_at(g, 1, w - 4, s5, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_shapes":
        return g
    if name == "no_subset":
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 3)
        paint_at(g, 5, 8, [(0, 0)], 5)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
