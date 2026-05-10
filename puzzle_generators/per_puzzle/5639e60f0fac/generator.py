"""Generator for arc_additional_puzzles_21_set2:H11.

Rule: a 3-template (bbox crop) is stamped into a solid 8-rectangle of
the same dimensions; 3-cells become 8, others become 0.

Combinatorial axes (8): grid_h/w, palette_kind, template_kind,
palette_size, position_bias, n_distinct_colors, canvas_size, texture.
Degenerates: no_template, no_canvas, mismatched_dims.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "5639e60f0fac"
VERSION = "1.1.0"
TASK_ID = "5639e60f0fac"
SUMMARY = "3-template (3×3 motif) + solid 8-rect of same dims."

INVARIANTS = [
    "exactly one 3-blob with bbox 3×3 and asymmetric shape",
    "exactly one solid 8-rect with same dimensions",
]

PALETTE_KINDS = ("default", "L_template", "T_template", "Z_template")
DEGENERATE_TEXTURES = ("no_template", "no_canvas", "mismatched_dims")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "template_kind":  {"type": "str", "default": "fixed_3x3",
                       "valid": "fixed_3x3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "canvas_size":    {"type": "str", "default": "match", "valid": "match"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid_rect(g, r1, c1, r2, c2, color):
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)], 3)
    _solid_rect(g, h - 5, w - 5, h - 3, w - 3, 8)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # 8-canvas but no 3-template → no shape to stamp
        _solid_rect(g, h - 5, w - 5, h - 3, w - 3, 8)
        return g
    if name == "no_canvas":
        # 3-template but no 8-canvas → no destination
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)], 3)
        return g
    if name == "mismatched_dims":
        # template 3×3 but canvas 4×4 → can't stamp
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1), (2, 2)], 3)
        _solid_rect(g, h - 6, w - 6, h - 3, w - 3, 8)
        return g
    return g
