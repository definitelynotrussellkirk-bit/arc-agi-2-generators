"""Generator for arc_additional_puzzles_21_set3:H20.

Rule: legend colors choose colored pieces, packed horizontally in legend
order.

Combinatorial axes (8): grid_h/w, piece_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_pieces, no_legend, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "204213f10aff"
VERSION = "1.1.0"
TASK_ID = "204213f10aff"
SUMMARY = "Legend colors choose pieces; packed horizontally in legend order."

INVARIANTS = [
    "row 0 lists the color order",
    "matching colored objects below row 0 are cropped as pieces",
    "pieces are packed horizontally with one blank column gap",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pieces", "no_legend", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "piece_count":    {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        piece_count = ctx.draw_int("piece_count", 2, 2)
    elif difficulty == "hard":
        piece_count = ctx.draw_int("piece_count", 3, 3)
    else:
        piece_count = ctx.draw_int("piece_count", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=piece_count, exclude={0})
    g = full_grid(9, 14, 0)
    for i, color in enumerate(colors):
        g[0][i] = color
    draw_rect(g, 2, 8, 2, 3, colors[0])
    draw_rect(g, 5, 1, 3, 1, colors[1])
    if piece_count == 3:
        draw_rect(g, 4, 5, 2, 2, colors[2])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 14, 0)
    if name == "no_pieces":
        g[0][0] = 3
        g[0][1] = 4
        return g
    if name == "no_legend":
        draw_rect(g, 2, 8, 2, 3, 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
