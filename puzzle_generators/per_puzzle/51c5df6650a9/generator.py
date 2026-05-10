"""Generator for arc_additional_puzzles_21_set12_bundle:M78.

Rule: row 0 has legend colors (in order); for each, find object with
that color in body; concat their bbox crops with 1-col gaps starting
at row 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_legend,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, missing_body_color, single_legend.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "51c5df6650a9"
VERSION = "1.1.0"
TASK_ID = "51c5df6650a9"
SUMMARY = "Row 0 has 3 legend colors + 3 distinct-color body blobs."

INVARIANTS = [
    "row 0 has 3 non-zero cells (legend)",
    "body has exactly 3 blobs each of legend colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "missing_body_color", "single_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_legend":       {"type": "int", "default": "3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "legend_top_blobs_body",
                       "valid": "legend_top_blobs_body"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
    g[0][0] = palette[0]; g[0][2] = palette[1]; g[0][4] = palette[2]
    paint_at(g, 3, 2, [(0, 0), (1, 0), (1, 1)], palette[0])
    paint_at(g, 6, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], palette[1])
    paint_at(g, 7, 9, [(0, 0), (1, 0)], palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # row 0 empty → no order/colors selected
        paint_at(g, 3, 2, [(0, 0), (1, 0), (1, 1)], 4)
        paint_at(g, 6, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
        paint_at(g, 7, 9, [(0, 0), (1, 0)], 7)
        return g
    if name == "missing_body_color":
        # legend has color C but body has no C-blob → packing skips, output incomplete
        g[0][0] = 4; g[0][2] = 6; g[0][4] = 7
        paint_at(g, 3, 2, [(0, 0), (1, 0), (1, 1)], 4)
        paint_at(g, 6, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
        # color 7 missing
        return g
    if name == "single_legend":
        # legend has only 1 color → packing degenerates to one crop
        g[0][0] = 4
        paint_at(g, 3, 2, [(0, 0), (1, 0), (1, 1)], 4)
        return g
    return g
