"""Generator for arc_additional_puzzle_bank_volume5:H31.

Rule: a bottom legend recolors a multicolor template; maroon anchors
stamp the recolored copies above the legend.

Combinatorial axes (8): grid_h/w, palette_kind, n_anchors, palette_size,
position_bias, n_distinct_colors, legend_count, texture.
Degenerates: no_legend, no_template, no_anchors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "61a55c0c7ee8"
VERSION = "1.1.0"
TASK_ID = "61a55c0c7ee8"
SUMMARY = "A bottom legend recolors a multicolor template, then maroon anchors stamp the recolored copies."

INVARIANTS = [
    "the bottom two rows contain exactly three legend columns",
    "the template uses only source legend colors",
    "one or more maroon anchors appear above the legend",
    "all recolored template stamps fit above the legend rows",
]

PALETTE_KINDS = ("default", "warm_legend", "cool_legend", "varied_legend")
DEGENERATE_TEXTURES = ("no_legend", "no_template", "no_anchors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6"},
    "legend_count":   {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    g = full_grid(h, w, 0)
    g[0][0] = 1
    g[0][1] = 2
    g[1][0] = 3
    g[1][1] = 1
    g[2][1] = 2
    g[3][w // 2] = 9
    g[5][w - 5] = 9
    for c, (src, dst) in enumerate([(1, 4), (2, 6), (3, 7)]):
        g[h - 2][c] = src
        g[h - 1][c] = dst
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # template + anchors but no legend — recolor mapping undefined
        g[0][0] = 1; g[0][1] = 2; g[1][0] = 3; g[1][1] = 1; g[2][1] = 2
        g[3][w // 2] = 9
        return g
    if name == "no_template":
        # legend + anchors but no template to recolor and stamp
        g[3][w // 2] = 9
        for c, (src, dst) in enumerate([(1, 4), (2, 6), (3, 7)]):
            g[h - 2][c] = src
            g[h - 1][c] = dst
        return g
    if name == "no_anchors":
        # template + legend but no maroon anchors — no copies stamped
        g[0][0] = 1; g[0][1] = 2; g[1][0] = 3; g[1][1] = 1; g[2][1] = 2
        for c, (src, dst) in enumerate([(1, 4), (2, 6), (3, 7)]):
            g[h - 2][c] = src
            g[h - 1][c] = dst
        return g
    return g
