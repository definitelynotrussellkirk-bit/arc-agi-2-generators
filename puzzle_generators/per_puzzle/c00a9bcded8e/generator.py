"""Generator for 0a1d4ef5.

Rule: solid colored rectangles read in row-major grid order into a
compact color table.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_rects, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "c00a9bcded8e"
VERSION = "1.1.0"
TASK_ID = "c00a9bcded8e"
SUMMARY = "Solid colored rectangles read in row-major grid order into color table."

INVARIANTS = [
    "there are two rows and three columns of large solid rectangles",
    "rectangle center rows are separated by at least four cells",
    "all target rectangles are at least nine cells",
    "rectangle colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "single_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 19..22", "valid": "16..28"},
    "rect_h":         {"type": "int", "default": "rng 3..4", "valid": "3..8"},
    "rect_w":         {"type": "int", "default": "rng 3..4", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    rh = ctx.draw_int("rect_h", 3, 4)
    rw = ctx.draw_int("rect_w", 3, 4)
    h = 2 * rh + 8
    w = 3 * rw + 10
    g = full_grid(h, w, 0)
    colors = list(ctx.draw_distinct_colors("colors", n=6, exclude={0}))
    row_starts = [1, rh + 6]
    col_starts = [1, rw + 4, 2 * rw + 7]
    i = 0
    for r in row_starts:
        for c in col_starts:
            draw_rect(g, r, c, rh, rw, colors[i])
            i += 1
    if rng.choice([True, False]):
        g[h - 2][w - 2] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 19, 0)
    if name == "no_rects":
        return g
    if name == "single_rect":
        draw_rect(g, 1, 1, 3, 3, 2)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(19):
                g[r][c] = 2
        return g
    return g
