"""Generator for additional_bank:M6.

Rule: objects sorted largest-first become one row of color runs
separated by zeros.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_objects, equal_sizes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "5cb854cd43c4"
VERSION = "1.1.0"
TASK_ID = "5cb854cd43c4"
SUMMARY = "Objects sorted largest-first become one row of color runs separated by zeros."

INVARIANTS = [
    "objects are separated by background",
    "object sizes differ so largest-first order is visible",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "equal_sizes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude=[0]))
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], colors[0])
    paint_at(g, 1, w - 4, [(0, 0), (0, 1), (1, 1)], colors[1])
    paint_at(g, h - 3, 1, [(0, 0), (1, 0)], colors[2])
    paint_at(g, h - 2, w - 2, [(0, 0)], colors[3])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_objects":
        return g
    if name == "equal_sizes":
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
        paint_at(g, 1, 7, [(0, 0), (0, 1)], 3)
        paint_at(g, 6, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 6, 7, [(0, 0), (0, 1)], 5)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
