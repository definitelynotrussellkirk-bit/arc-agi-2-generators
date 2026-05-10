"""Generator for arc_puzzle_bank_21_set15:S15_M4.

Rule: marker colors 3-6 choose identity, mirror, flip, or rotation
stamps of a color-2 template.

Combinatorial axes (8): grid_h, grid_w, palette_kind, include_all_commands,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_markers, marker_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "4296e507c770"
VERSION = "1.1.0"
TASK_ID = "4296e507c770"
SUMMARY = "Marker colors 3-6 choose identity, mirror, flip, or rotation stamps of a color-2 template."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 template object",
    "marker colors 3 through 6 are singleton command anchors",
    "all command anchors have room for their transformed template footprints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_markers", "marker_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..16", "valid": "11..20"},
    "grid_w":         {"type": "int", "default": "rng 16..19", "valid": "14..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "include_all_commands": {"type": "bool", "default": "rng",
                             "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "template_corner",
                       "valid": "template_corner"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("height", 13, 14)
        w = ctx.draw_int("width", 16, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 15, 16)
        w = ctx.draw_int("width", 18, 19)
    else:
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 16, 19)
    include_all = ctx.draw_choice("include_all_commands", [False, True])
    g = full_grid(h, w, 0)

    paint_at(g, 1, 1, TEMPLATE, 2)
    commands = [(3, 1, w - 5), (4, h - 5, w - 5), (5, h - 5, 5), (6, 5, w - 9)]
    for color, r, c in commands[:4 if include_all else 3]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 17
    g = full_grid(h, w, 0)
    if name == "no_template":
        # marker anchors exist but no color-2 template → nothing to stamp from
        for color, r, c in [(3, 1, w - 5), (4, h - 5, w - 5), (5, h - 5, 5)]:
            g[r][c] = color
        return g
    if name == "no_markers":
        # template exists but no command markers → nothing decides the transform
        paint_at(g, 1, 1, TEMPLATE, 2)
        return g
    if name == "marker_at_edge":
        # marker placed at the grid edge → transformed footprint clips out of bounds
        paint_at(g, 1, 1, TEMPLATE, 2)
        g[0][w - 1] = 3
        g[h - 1][0] = 4
        return g
    return g
