"""Generator for arc_additional_puzzles_21_set8:M56.

Rule: locate the solid rectangle and the non-rectangular shape; output
the cropped shape recolored using the rectangle's color.

Combinatorial axes (8): grid_h/w, palette_kind, num_rects, num_shapes,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_rect, no_shape, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "e927138d8305"
VERSION = "1.1.0"
TASK_ID = "e927138d8305"
SUMMARY = "Find solid rectangles and non-rectangular shapes; output the last shape crop recolored by the last rectangle."

INVARIANTS = [
    "at least one solid rectangle and one non-rectangular shape exist",
    "the non-rectangular shape is separated and appears after the rectangle in reading order",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_rect", "no_shape", "all_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_rects":      {"type": "int", "default": "1", "valid": "1"},
    "num_shapes":     {"type": "int", "default": "1", "valid": "1"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    rect_color, shape_color = ctx.draw_distinct_colors("colors", n=2, exclude=[0])
    g = full_grid(h, w, 0)
    draw_rect(g, 1, 1, 2, 3, rect_color)
    for dr, dc in [(0, 0), (0, 2), (1, 0), (2, 1)]:
        g[h - 4 + dr][w - 5 + dc] = shape_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_rect":
        # only the non-rectangular shape — no source color to recolor with
        for dr, dc in [(0, 0), (0, 2), (1, 0), (2, 1)]:
            g[h - 4 + dr][w - 5 + dc] = 5
        return g
    if name == "no_shape":
        # only a rectangle — nothing to recolor
        draw_rect(g, 1, 1, 2, 3, 4)
        return g
    if name == "all_same_color":
        # rect and shape share a color — recoloring is a no-op
        draw_rect(g, 1, 1, 2, 3, 5)
        for dr, dc in [(0, 0), (0, 2), (1, 0), (2, 1)]:
            g[h - 4 + dr][w - 5 + dc] = 5
        return g
    return g
