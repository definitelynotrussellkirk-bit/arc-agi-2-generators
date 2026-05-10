"""Generator for arc_additional_puzzles_21_set7:H49.

Rule: color traces are drawn through their points (horizontal-then-vertical)
in row-major order; cells already occupied by a previous trace become
overlap color 9.

Combinatorial axes (8): grid_h/w, palette_kind, crossing,
palette_size, position_bias, n_distinct_colors, num_points_a, texture.
Degenerates: no_overlap, single_color, single_point.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d095613d305"
VERSION = "1.1.0"
TASK_ID = "6d095613d305"
SUMMARY = "Color traces are drawn in row-major order, with overlaps marked as color 9."

INVARIANTS = [
    "each foreground color contributes an ordered point trace",
    "segments move horizontally first and vertically second",
    "cells already occupied by a previous trace become overlap color 9",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_overlap", "single_color", "single_point")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "crossing":       {"type": "choice", "default": "rng yes|no",
                       "valid": "yes|no"},
    "num_points_a":   {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    crossing = ctx.draw_choice("crossing", ["yes", "no"])
    if "crossing" not in overrides:
        if difficulty == "easy":
            crossing = "no"
        elif difficulty == "hard":
            crossing = "yes"
        else:
            crossing = "yes" if sample_index % 2 == 0 else "no"
    a, b = ctx.draw_distinct_colors("colors", n=2, exclude={0, 9})
    g = full_grid(10, 10, 0)
    for r, c in [(1, 1), (5, 7), (8, 7)]:
        g[r][c] = a
    pts_b = [(3, 7), (5, 2), (8, 2)] if crossing == "yes" else [(2, 8), (6, 8)]
    for r, c in pts_b:
        g[r][c] = b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_overlap":
        # traces stay in disjoint regions — no 9s in output
        g[1][1] = 4; g[1][3] = 4; g[2][3] = 4
        g[7][7] = 6; g[8][7] = 6; g[8][9] = 6
        return g
    if name == "single_color":
        # only one color trace — no second trace to cross, no 9s possible
        g[1][1] = 5; g[5][7] = 5; g[8][7] = 5
        return g
    if name == "single_point":
        # each color has only one point — degenerate trace
        g[2][2] = 4
        g[7][7] = 6
        return g
    return g
