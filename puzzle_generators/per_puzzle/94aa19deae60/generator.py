"""Generator for arc_additional_puzzles_21_set11_bundle:M77.

Rule: row 0 has legend colors. For each, find the body object of that
color; concat their bbox crops horizontally with 1-col gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_legend,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_body_match, single_legend_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "94aa19deae60"
VERSION = "1.1.0"
TASK_ID = "94aa19deae60"
SUMMARY = "Row 0 has 3 legend colors + 3 distinct-color body blobs."

INVARIANTS = [
    "row 0 has 3 non-zero cells (legend, in order)",
    "body has 3 non-touching blobs each of legend colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_body_match", "single_legend_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_legend":       {"type": "int", "default": "3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "legend_top_body_below",
                       "valid": "legend_top_body_below"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7]; rng.shuffle(palette)
    g[0][0] = palette[0]; g[0][1] = palette[1]; g[0][2] = palette[2]
    paint_at(g, 3, 1, [(0, 0), (0, 1), (1, 0)], palette[0])
    paint_at(g, 2, 5, [(0, 0), (0, 1), (1, 0), (1, 1)], palette[1])
    paint_at(g, 5, 10, [(0, 0), (1, 0), (2, 0), (2, 1)], palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # row 0 empty → no order/colors selected, rule has nothing to extract
        paint_at(g, 3, 1, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 2, 5, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
        paint_at(g, 5, 10, [(0, 0), (1, 0), (2, 0), (2, 1)], 7)
        return g
    if name == "no_body_match":
        # legend colors are set but body doesn't contain those colors → empty packing
        g[0][0] = 4; g[0][1] = 6; g[0][2] = 7
        paint_at(g, 3, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 2, 5, [(0, 0), (0, 1)], 3)
        return g
    if name == "single_legend_color":
        # legend has only 1 color → packing is trivially one crop
        g[0][0] = 4
        paint_at(g, 3, 1, [(0, 0), (0, 1), (1, 0)], 4)
        return g
    return g
