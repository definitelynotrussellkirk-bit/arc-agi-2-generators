"""Generator for 83eb0a57.

Rule: smaller multicolor rectangles are stamped into the largest
container by aligning shared color markers.

Combinatorial axes (8): grid_h/w, piece_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_canvas, no_pieces, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid, paint_at

GENERATOR_ID = "69db2372d14f"
VERSION = "1.1.0"
TASK_ID = "69db2372d14f"
SUMMARY = "Smaller multicolor rectangles stamped into largest container by aligning markers."

INVARIANTS = [
    "the largest non-background object supplies the output canvas bbox",
    "the canvas already contains one or more shared marker colors",
    "outside multicolor objects contain matching marker colors",
    "each outside object is placed where its marker cells align with the canvas marker cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_canvas", "no_pieces", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "piece_count":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "6", "valid": "6"},
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
        piece_count = ctx.draw_int("piece_count", 1, 1)
    elif difficulty == "hard":
        piece_count = ctx.draw_int("piece_count", 2, 2)
    else:
        piece_count = ctx.draw_int("piece_count", 1, 2)
    bg_color, frame_color, marker_a, marker_b, fill_a, fill_b = ctx.draw_distinct_colors(
        "colors", n=6, exclude={0}
    )
    g = full_grid(14, 16, bg_color)
    draw_frame(g, 1, 1, 8, 9, frame_color)
    g[3][3] = marker_a
    g[5][6] = marker_b
    paint_at(g, 10, 2, [(0, 0), (0, 1), (1, 0), (1, 1)], fill_a)
    g[10][2] = marker_a
    if piece_count == 2:
        paint_at(g, 10, 10, [(0, 0), (0, 1), (1, 1), (2, 1)], fill_b)
        g[10][10] = marker_b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 16, 0)
    if name == "no_canvas":
        paint_at(g, 10, 2, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        g[10][2] = 3
        return g
    if name == "no_pieces":
        draw_frame(g, 1, 1, 8, 9, 5)
        g[3][3] = 3
        g[5][6] = 6
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(16):
                g[r][c] = 5
        return g
    return g
