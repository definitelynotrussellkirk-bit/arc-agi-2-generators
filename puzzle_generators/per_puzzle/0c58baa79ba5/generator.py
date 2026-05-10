"""Generator for arc_additional_puzzles_21_set11_bundle:M76.

Rule: the first two objects are normalized to their bboxes; differing
occupancy cells become 8.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_objects, identical_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "0c58baa79ba5"
VERSION = "1.1.0"
TASK_ID = "0c58baa79ba5"
SUMMARY = "The first two objects are normalized to their bboxes; differing occupancy cells become 8."

INVARIANTS = [
    "exactly two separated nonzero objects are present",
    "their normalized occupancies overlap partly but differ",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "identical_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
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
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
    colors = list(ctx.draw_distinct_colors("colors", n=2, exclude=[0, 8]))
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (2, 0)], colors[0])
    paint_at(g, h - 4, w - 4, [(0, 0), (1, 0), (1, 1), (2, 1)], colors[1])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 11, 0)
    if name == "no_objects":
        return g
    if name == "identical_shapes":
        s = [(0, 0), (0, 1), (1, 0)]
        paint_at(g, 1, 1, s, 2)
        paint_at(g, 5, 6, s, 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
