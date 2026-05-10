"""Generator for arc_puzzle_bank_twentythird21:E157.

Rule: each non-zero cell in the bottom row paints an up-left diagonal
of that color (until a grid edge).

Combinatorial axes (8): grid_h/w, palette_kind, n_markers, palette_size,
position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_markers, marker_at_left_edge, body_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "eca9d989b5bd"
VERSION = "1.1.0"
TASK_ID = "eca9d989b5bd"
SUMMARY = "Bottom row has 1-3 colored markers; rest of the grid is empty."

INVARIANTS = [
    "background is 0",
    "1-3 colored markers on the bottom row at distinct columns",
    "all other cells are 0",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_markers", "marker_at_left_edge", "body_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "bottom_row",
                       "valid": "bottom_row"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "marker_density": {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    n = ctx.draw_int("n_markers", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for c, color in zip(cols, colors):
        g[h - 1][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # empty grid — no diagonals to paint
        return g
    if name == "marker_at_left_edge":
        # marker at column 0 → diagonal has length 1 (degenerate)
        g[h - 1][0] = 5
        return g
    if name == "body_already_filled":
        # body has cells already → invariant violated
        g[h - 1][3] = 4
        g[2][1] = 6  # body cell, should not exist
        g[3][5] = 7
        return g
    return g
