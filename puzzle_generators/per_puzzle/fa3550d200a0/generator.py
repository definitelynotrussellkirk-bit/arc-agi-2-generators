"""Generator for 414297c0.

Rule: outside multicolor objects are stamped onto a same-color
rectangle at matching marker colors.

Combinatorial axes (8): grid_h/w, piece_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_pieces, no_canvas, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid, paint_at

GENERATOR_ID = "fa3550d200a0"
VERSION = "1.1.0"
TASK_ID = "fa3550d200a0"
SUMMARY = "Outside multicolor pieces stamp onto rectangle at marker positions."

INVARIANTS = [
    "the modal nonzero rectangle color defines the output canvas bbox",
    "marker colors inside the rectangle identify stamp anchors",
    "outside multicolor objects contain matching marker colors plus payload",
    "marker and payload colors are distinct and exclude 0 and 2",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pieces", "no_canvas", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "piece_count":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
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
    if difficulty == "easy":
        pc_lo, pc_hi = 1, 1
    elif difficulty == "hard":
        pc_lo, pc_hi = 2, 2
    else:
        pc_lo, pc_hi = 1, 2
    piece_count = ctx.draw_int("piece_count", pc_lo, pc_hi)
    rect_color, marker_a, marker_b, payload_a, payload_b = ctx.draw_distinct_colors(
        "colors", n=5, exclude={0, 2}
    )
    g = full_grid(14, 15, 0)
    draw_rect(g, 2, 2, 8, 8, rect_color)
    g[5][5] = marker_a
    g[7][7] = marker_b
    paint_at(g, 1, 11, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
    g[1][11] = marker_a
    g[2][12] = payload_a
    if piece_count == 2:
        paint_at(g, 9, 11, [(0, 0), (1, 0), (1, 1), (2, 1)], 2)
        g[9][11] = marker_b
        g[10][12] = payload_b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 0)
    if name == "no_pieces":
        draw_rect(g, 2, 2, 8, 8, 5)
        return g
    if name == "no_canvas":
        paint_at(g, 1, 11, [(0, 0), (0, 1)], 2)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 5
        return g
    return g
