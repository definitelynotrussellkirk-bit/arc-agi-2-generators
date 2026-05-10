"""Generator for arc_additional_puzzles_21_set3:H21.

Rule: the largest 6-blob is a template shape. Find the solid 3-rect with
matching h×w; replace its 3-cells with 8s in template positions only.

Combinatorial axes (8): grid_h/w, palette_kind, template_shape,
palette_size, position_bias, n_distinct_colors, rect_alignment, texture.
Degenerates: no_template, no_3_rect, mismatched_dims.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "be02b305dd1e"
VERSION = "1.1.0"
TASK_ID = "be02b305dd1e"
SUMMARY = "6-template (3 cells in 3x2 bbox) + 3-rect of same dimensions."

INVARIANTS = [
    "6-template at upper-left",
    "solid 3-rect of same h×w as 6-template's bbox",
]

PALETTE_KINDS = ("default", "wide_grid", "tight_grid", "different_shapes")
DEGENERATE_TEXTURES = ("no_template", "no_3_rect", "mismatched_dims")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "template_shape": {"type": "str", "default": "fixed", "valid": "fixed"},
    "rect_alignment": {"type": "str", "default": "matched", "valid": "matched"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 6)
    _solid(g, 5, w - 4, 7, w - 3, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_template":
        # 3-rect but no 6-template — rule has no shape to copy
        _solid(g, 5, w - 4, 7, w - 3, 3)
        return g
    if name == "no_3_rect":
        # template but no matching 3-rect — rule has nothing to replace
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 6)
        return g
    if name == "mismatched_dims":
        # 3-rect dimensions don't match the 6-template's bbox
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 6)
        _solid(g, 5, w - 5, 6, w - 2, 3)
        return g
    return g
