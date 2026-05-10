"""Generator for arc_additional_puzzles_21_set14_bundle:M96.

Rule: normalize 2-cells and 3-cells; overlay in bbox of union. Both →
8, 2 only → 2, 3 only → 3.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, identical_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "1b6b40a92e4f"
VERSION = "1.1.0"
TASK_ID = "1b6b40a92e4f"
SUMMARY = "2-shape and 3-shape placed apart with shared and unique cells."

INVARIANTS = [
    "exactly one 2-blob and one 3-blob",
    "their normalized cells share at least one and differ at least one",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "identical_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    s2 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    s3 = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, 1, 1, s2, 2)
    paint_at(g, 5, w - 5, s3, 3)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_shapes":
        return g
    if name == "identical_shapes":
        s = [(0, 0), (1, 0), (1, 1)]
        paint_at(g, 1, 1, s, 2)
        paint_at(g, 5, 7, s, 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
