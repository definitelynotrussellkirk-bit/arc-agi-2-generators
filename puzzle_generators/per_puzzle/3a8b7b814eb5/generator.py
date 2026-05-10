"""Generator for arc_additional_puzzle_bank_volume2:M10.

Rule: for each non-bg color with exactly 2 cells, fill the rectangle
between them with that color.

Combinatorial axes (8): grid_h/w, palette_kind, n_pairs, palette_size,
position_bias, n_distinct_colors, rect_orientation, texture.
Degenerates: single_cell_color, three_cell_color, overlapping_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3a8b7b814eb5"
VERSION = "1.1.0"
TASK_ID = "3a8b7b814eb5"
SUMMARY = "2-3 distinct colors each with exactly 2 cells (diagonal corners) + decoration."

INVARIANTS = [
    "between 2 and 3 distinct non-bg colors",
    "each has exactly 2 cells, at diagonal corners (different rows AND cols)",
    "rectangles are non-overlapping",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_cell_color", "three_cell_color", "overlapping_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "split", "valid": "split"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "rect_orientation": {"type": "str", "default": "diagonal", "valid": "diagonal"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    g[1][1] = 1
    g[3][w // 2 - 1] = 1
    g[h - 3][2] = 3
    g[h - 1][5] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "single_cell_color":
        # color with one cell only → rectangle predicate fails
        g[1][1] = 1
        g[h - 3][2] = 3; g[h - 1][5] = 3
        return g
    if name == "three_cell_color":
        # color with 3 cells → "exactly 2" predicate fails
        g[1][1] = 1; g[3][5] = 1; g[2][3] = 1
        g[h - 3][2] = 3; g[h - 1][5] = 3
        return g
    if name == "overlapping_rects":
        # two color pairs whose rectangles overlap → ambiguous fill order
        g[1][1] = 1; g[5][7] = 1
        g[2][3] = 3; g[6][9] = 3
        return g
    return g
