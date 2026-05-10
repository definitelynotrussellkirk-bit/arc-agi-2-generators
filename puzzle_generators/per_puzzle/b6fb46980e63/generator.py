"""Generator for arc_additional_puzzles_21_set7:H45 — hole-count legend recolor.

Rule: top legend colors recolor lower components by whether they have
0, 1, or 2 holes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, all_same_holes, missing_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b6fb46980e63"
VERSION = "1.1.0"
TASK_ID = "b6fb46980e63"
SUMMARY = "Top legend colors recolor lower components by whether they have 0, 1, or 2 holes."

INVARIANTS = [
    "background is 0",
    "the first three nonzero top-row cells are the legend colors",
    "lower components include one 0-hole, one 1-hole, and one 2-hole shape",
    "components are separated by at least one blank cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "all_same_holes", "missing_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "legend_with_3_hole_classes",
                       "valid": "legend_with_3_hole_classes"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, r0, c0, pattern, color):
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            if ch == "1":
                g[r0 + r][c0 + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 14, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    for c, color in enumerate(legend):
        g[0][c] = color

    body = 5
    _paint(g, 2, 1, ["111", "010"], body)
    _paint(g, 2, 6, ["111", "101", "111"], body)
    _paint(g, 7, 4, ["11111", "10101", "11111"], body)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    body = 5
    if name == "no_legend":
        # row 0 empty → no recolor mapping for hole counts
        _paint(g, 2, 1, ["111", "010"], body)
        _paint(g, 2, 6, ["111", "101", "111"], body)
        _paint(g, 7, 4, ["11111", "10101", "11111"], body)
        return g
    if name == "all_same_holes":
        # all 3 components share hole count → all map to same legend color
        legend = [4, 6, 3]
        for c, color in enumerate(legend): g[0][c] = color
        # all 0-hole shapes
        _paint(g, 2, 1, ["111", "010"], body)        # 0 holes
        _paint(g, 5, 1, ["111", "010"], body)        # 0 holes
        _paint(g, 8, 1, ["111", "010"], body)        # 0 holes
        return g
    if name == "missing_components":
        # only 2 of 3 hole classes present → 1 legend slot unused
        legend = [4, 6, 3]
        for c, color in enumerate(legend): g[0][c] = color
        _paint(g, 2, 1, ["111", "010"], body)        # 0 holes
        _paint(g, 2, 6, ["111", "101", "111"], body) # 1 hole
        # 2-hole missing
        return g
    return g
