"""Generator for arc_additional_puzzles_21_set10_bundle:M66.

Rule: objects are sorted by reading order (top-left position) and
encoded as rows of their color repeated by size.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_object, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "56362868a163"
VERSION = "1.1.0"
TASK_ID = "56362868a163"
SUMMARY = "Objects are sorted by top-left position and encoded as rows of their color repeated by size."

INVARIANTS = [
    "objects are separated and appear in reading order",
    "object sizes vary, making row lengths visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "corners", "valid": "corners"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "size_spread":    {"type": "str", "default": "varied", "valid": "varied"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 13)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude=[0]))
    g = full_grid(h, w, 0)
    specs = [
        (1, 1, [(0, 0), (0, 1), (1, 0)], colors[0]),
        (1, w - 4, [(0, 0), (1, 0)], colors[1]),
        (h - 4, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], colors[2]),
        (h - 3, w - 3, [(0, 0)], colors[3]),
    ]
    for top, left, cells, color in specs:
        paint_at(g, top, left, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "equal_sizes":
        # all objects have the same size → row-length signal collapses
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
        paint_at(g, 1, w - 4, [(0, 0), (0, 1)], 3)
        paint_at(g, h - 3, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, h - 3, w - 4, [(0, 0), (0, 1)], 5)
        return g
    if name == "single_object":
        # only one object → no ordering, output is a single row
        paint_at(g, 2, 3, [(0, 0), (0, 1), (0, 2), (1, 1)], 6)
        return g
    if name == "no_objects":
        # empty grid → no rows to emit
        return g
    return g
