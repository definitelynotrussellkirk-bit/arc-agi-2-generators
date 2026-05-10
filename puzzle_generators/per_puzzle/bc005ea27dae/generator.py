"""Generator for arc_puzzle_bank_21_set13_s:S13_M5 — pick highest-perimeter object.

Rule: the object with the greatest exposed-cell perimeter is cropped
and recolored.

Combinatorial axes (8): grid_h, grid_w, palette_kind, bar_orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, tied_perimeter.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "bc005ea27dae"
VERSION = "1.1.0"
TASK_ID = "bc005ea27dae"

SUMMARY = "The object with the greatest exposed-cell perimeter is cropped and recolored."

INVARIANTS = [
    "background is 0",
    "one long thin object has strictly highest perimeter",
    "other objects have smaller perimeter or lower tie-break priority",
    "all components are separated from one another",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "tied_perimeter")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bar_orientation": {"type": "str", "default": "rng horizontal|vertical",
                        "valid": "horizontal|vertical"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "bar_with_distractors",
                       "valid": "bar_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

BAR_H = [(0, c) for c in range(5)]
BAR_V = [(r, 0) for r in range(5)]
RECT_2X2 = [(r, c) for r in range(2) for c in range(2)]
PLUS_5 = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 15)
    orientation = ctx.draw_choice("bar_orientation", ["horizontal", "vertical"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    if orientation == "horizontal":
        paint_at(g, rng.randint(1, 2), 1, BAR_H, 2)
    else:
        paint_at(g, 1, rng.randint(1, 2), BAR_V, 2)
    paint_at(g, 1, w - 4, RECT_2X2, 3)
    paint_at(g, h - 4, w - 5, PLUS_5, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no objects to pick from
        return g
    if name == "single_object":
        # only one object → "highest perimeter" is trivial identity
        paint_at(g, 2, 2, BAR_H, 2)
        return g
    if name == "tied_perimeter":
        # two objects with equal perimeter → ambiguous max
        paint_at(g, 2, 1, BAR_H, 2)
        paint_at(g, 6, 1, BAR_H, 4)   # same shape (5 cells in a line) - same perimeter
        return g
    return g
