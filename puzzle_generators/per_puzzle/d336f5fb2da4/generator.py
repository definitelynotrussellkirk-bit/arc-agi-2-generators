"""Generator for arc_additional_puzzle_bank_volume20:H139.

Rule: a control-transformed blue source shape is repeat-stamped in cyan
along the vector defined by markers 2 and 3.

Combinatorial axes (9): grid_h/w, palette_kind, control_color,
source_anchor, marker_step, palette_size, position_bias,
n_distinct_colors, texture.
Degenerates: no_source, markers_collide, source_too_big.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d336f5fb2da4"
VERSION = "1.1.0"
TASK_ID = "d336f5fb2da4"
SUMMARY = "A control-transformed blue source shape is repeat-stamped in cyan along the vector from marker 2 to marker 3."

INVARIANTS = [
    "one color-1 source shape is present",
    "one control marker is 4, 6, or 7",
    "markers 2 and 3 define a positive repeat step",
    "at least two full stamps fit before leaving the grid",
]

PALETTE_KINDS = ("default", "control_4", "control_6", "control_7")
DEGENERATE_TEXTURES = ("no_source", "markers_collide", "source_too_big")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 14..20", "valid": "12..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control_color":  {"type": "int", "default": "rng 4|6|7", "valid": "4|6|7"},
    "marker_step":    {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        w = ctx.draw_int("grid_w", 14, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 18, 20)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 14, 20)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 1)
    g[0][w - 1] = rng.choice([4, 6, 7])
    row = h - 4
    g[row][1] = 2
    g[row][4] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 16
    g = full_grid(h, w, 0)
    if name == "no_source":
        # markers + control but no blue source to stamp
        g[0][w - 1] = 4
        g[h - 4][1] = 2
        g[h - 4][4] = 3
        return g
    if name == "markers_collide":
        # 2 and 3 at same cell — zero step vector
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 1)
        g[0][w - 1] = 6
        g[h - 4][3] = 2
        g[h - 4][3] = 3
        return g
    if name == "source_too_big":
        # source spans most of the grid — only one stamp fits
        for r in range(2, h - 4):
            for c in range(1, w - 4):
                g[r][c] = 1
        g[0][w - 1] = 7
        g[h - 2][1] = 2
        g[h - 2][3] = 3
        return g
    return g
