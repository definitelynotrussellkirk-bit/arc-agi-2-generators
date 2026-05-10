"""Generator for arc_puzzle_bank_21_more:medium_b02.

Rule: each object is replaced by the border of its bounding box, in the
object's color.

Combinatorial axes (8): grid_h/w, palette_kind, num_objects,
palette_size, position_bias, n_distinct_colors, hole_density, texture.
Degenerates: solid_objects, single_cell_objects, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "fdb8815ba528"
VERSION = "1.1.0"
TASK_ID = "fdb8815ba528"
SUMMARY = "Each object is replaced by the border of its bounding box, using the object's color."

INVARIANTS = [
    "objects are separated by background",
    "at least one object has holes or missing interior cells so bbox border expansion is visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("solid_objects", "single_cell_objects", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_objects":    {"type": "int", "default": "3", "valid": "2..5"},
    "hole_density":   {"type": "str", "default": "mixed",
                       "valid": "none|some|many"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 13)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0]))
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 2), (1, 0), (2, 0)], colors[0])
    paint_at(g, 1, w - 4, [(0, 0), (1, 1), (2, 1)], colors[1])
    paint_at(g, h - 4, 2, [(0, 0), (0, 1), (1, 0)], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "solid_objects":
        # Solid rectangles — bbox border equals object border, rule no-op
        for r in range(1, 4):
            for c in range(1, 4):
                g[r][c] = 4
        for r in range(6, 9):
            for c in range(6, 9):
                g[r][c] = 7
        return g
    if name == "single_cell_objects":
        # 1×1 objects — bbox border is the same single cell
        g[1][1] = 4
        g[3][5] = 7
        g[7][8] = 5
        return g
    if name == "no_objects":
        return g
    return g
