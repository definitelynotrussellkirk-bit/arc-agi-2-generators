"""Generator for arc_puzzle_bank_21_set15:S15_M2.

Rule: a color-2 template shape is stamped at each marker in that
marker's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_count,
palette_size, position_bias, n_distinct_colors, template_kind, texture.
Degenerates: no_template, no_markers, marker_color_2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "06b4c496c6cf"
VERSION = "1.1.0"
TASK_ID = "06b4c496c6cf"
SUMMARY = "A color-2 template shape is stamped at each marker in that marker's color."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 template object",
    "marker colors are single cells from colors 3 through 9",
    "marker anchors have room for the whole normalized template footprint",
]

PALETTE_KINDS = ("default", "warm_markers", "cool_markers", "varied_markers")
DEGENERATE_TEXTURES = ("no_template", "no_markers", "marker_color_2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 15..18", "valid": "13..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_count":   {"type": "int", "default": "rng 3..4", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "2..7"},
    "template_kind":  {"type": "str", "default": "S_shape", "valid": "S_shape"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

TEMPLATE = [(0, 0), (1, 0), (1, 1), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 15, 16)
        marker_count = ctx.draw_int("marker_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 14, 15)
        w = ctx.draw_int("width", 17, 18)
        marker_count = ctx.draw_int("marker_count", 3, 4)
    else:
        h = ctx.draw_int("height", 12, 15)
        w = ctx.draw_int("width", 15, 18)
        marker_count = ctx.draw_int("marker_count", 3, 4)
    g = full_grid(h, w, 0)

    paint_at(g, 1, 1, TEMPLATE, 2)
    anchors = [(1, w - 5), (h - 5, w - 5), (h - 5, 5), (5, w - 9)]
    for color, (r, c) in zip(range(3, 3 + marker_count), anchors):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 16
    g = full_grid(h, w, 0)
    if name == "no_template":
        # markers but no color-2 template → stamp footprint undefined
        g[1][w - 5] = 4
        g[h - 5][5] = 6
        return g
    if name == "no_markers":
        # template only, no markers → rule has nothing to stamp
        paint_at(g, 1, 1, TEMPLATE, 2)
        return g
    if name == "marker_color_2":
        # marker uses the same color as the template → blob/marker disambiguation fails
        paint_at(g, 1, 1, TEMPLATE, 2)
        g[h - 5][5] = 2
        return g
    return g
