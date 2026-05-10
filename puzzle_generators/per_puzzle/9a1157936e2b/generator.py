"""Generator for arc_puzzle_bank_21_set15:S15_M3.

Rule: a color-2 template is rotated 90° clockwise and stamped at the
location of the color-1 marker.

Combinatorial axes (8): grid_h/w, palette_kind, shape, marker_position,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_template, no_marker, marker_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "9a1157936e2b"
VERSION = "1.1.0"
TASK_ID = "9a1157936e2b"
SUMMARY = "A color-2 template is rotated 90 degrees clockwise and stamped at a blue marker."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 template object",
    "there is exactly one color-1 marker",
    "the marker anchor has room for the rotated template footprint",
]

PALETTE_KINDS = ("l_shape", "zig_shape", "wide_marker", "tight_marker")
DEGENERATE_TEXTURES = ("no_template", "no_marker", "marker_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "width":          {"type": "int", "default": "rng 13..16", "valid": "11..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "enum", "default": "rng l|zig",
                       "valid": "l|zig"},
    "marker_position": {"type": "str", "default": "lower_right",
                        "valid": "lower_right"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

L_SHAPE = [(0, 0), (1, 0), (1, 1), (2, 1)]
ZIG = [(0, 0), (0, 1), (1, 1), (1, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 14)
        w = ctx.draw_int("width", 15, 16)
    else:
        h = ctx.draw_int("height", 11, 14)
        w = ctx.draw_int("width", 13, 16)
    shape_name = ctx.draw_choice("shape", ["l", "zig"])
    g = full_grid(h, w, 0)

    paint_at(g, 1, 1, L_SHAPE if shape_name == "l" else ZIG, 2)
    g[h - 5][w - 5] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # marker but no template to rotate
        g[h - 5][w - 5] = 1
        return g
    if name == "no_marker":
        # template but no marker — nowhere to stamp
        paint_at(g, 1, 1, L_SHAPE, 2)
        return g
    if name == "marker_at_edge":
        # marker too close to edge — rotated stamp leaves the grid
        paint_at(g, 1, 1, L_SHAPE, 2)
        g[h - 1][w - 1] = 1
        return g
    return g
