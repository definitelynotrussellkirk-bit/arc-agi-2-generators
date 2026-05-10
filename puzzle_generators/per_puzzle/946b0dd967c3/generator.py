"""Generator for arc_additional_puzzles_21_set13_bundle:M89.

Rule: objects sorted by increasing size are repainted with rank colors
starting at 2 (smallest=2, next=3, ...).

Combinatorial axes (8): grid_h/w, palette_kind, n_objects, palette_size,
position_bias, n_distinct_colors, size_diversity, texture.
Degenerates: tied_sizes, single_object, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import L_TROMINO_SE, SQUARE_2X2

GENERATOR_ID = "946b0dd967c3"
VERSION = "1.1.0"
TASK_ID = "946b0dd967c3"
SUMMARY = "Objects sorted by increasing size are repainted with rank colors starting at 2."

INVARIANTS = [
    "objects are separated by background",
    "object sizes are distinct to make rank order unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("tied_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "size_diversity": {"type": "str", "default": "varied", "valid": "varied"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude=[0]))
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0)], colors[0])
    paint_at(g, 1, w - 3, [(0, 0), (1, 0)], colors[1])
    paint_at(g, h - 4, 1, L_TROMINO_SE, colors[2])
    paint_at(g, h - 4, w - 4, SQUARE_2X2, colors[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # multiple objects of equal size → rank order ambiguous
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 1, w - 3, [(0, 0), (0, 1)], 6)
        paint_at(g, h - 3, 1, [(0, 0), (0, 1)], 7)
        return g
    if name == "single_object":
        # only 1 object — rank trivially 2
        paint_at(g, 3, 3, SQUARE_2X2, 5)
        return g
    if name == "no_objects":
        # empty grid — nothing to rank
        return g
    return g
