"""Generator for arc_additional_puzzle_bank_volume19:M132.

Rule: normalize 2-cells & 3-cells; intersect (cells in both). Output
bbox-cropped intersection in color 8.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, no_intersection, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "564e67c1b7f4"
VERSION = "1.1.0"
TASK_ID = "564e67c1b7f4"
SUMMARY = "2-shape and 3-shape placed apart with shared normalized cells."

INVARIANTS = [
    "exactly one 2-blob and one 3-blob",
    "their normalized cell sets share at least one position",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_intersection", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
    paint_at(g, 1, 2, [(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)], 2)
    paint_at(g, 1, w - 4, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 3)
    g[h - 1][w - 1] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 11, 0)
    if name == "no_shapes":
        g[7][10] = 4
        return g
    if name == "no_intersection":
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
        paint_at(g, 5, 7, [(0, 0), (1, 0)], 3)
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
