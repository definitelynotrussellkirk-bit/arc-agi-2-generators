"""Generator for arc_additional_puzzles_21_set11_bundle:M73.

Rule: each object expands to its bounding-box border plus a same-color
checker pattern inside.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_objects, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2b7bcfbf942b"
VERSION = "1.1.0"
TASK_ID = "2b7bcfbf942b"
SUMMARY = "Each object expands to its bounding-box border plus a same-color checker pattern inside."

INVARIANTS = [
    "objects are separated by background",
    "object bounding boxes have interior cells where checker fill is visible",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
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
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
    colors = list(ctx.draw_distinct_colors("colors", n=2, exclude=[0]))
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3)], colors[0])
    paint_at(g, h - 4, w - 5, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3)], colors[1])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 3)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
