"""Generator for arc_additional_puzzles_21_set12_bundle:E80 — Mirror left half across full-9 column.

Rule: find the full-height col of 9s; for each non-bg cell on the
left side at (r, c), set (r, 2*gc - c) on the right side to that
color (if in-bounds).

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide, no_shape, cells_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "02dc25c0440b"
VERSION = "1.1.0"
TASK_ID = "02dc25c0440b"
SUMMARY = "Full-height col of 9s near middle; left side has a small shape."

INVARIANTS = [
    "exactly 1 full-height col of 9s",
    "left side has a small connected non-bg shape",
    "right side is empty (so mirror is visible)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "no_shape", "cells_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "vertical_9guide_with_left_shape",
                       "valid": "vertical_9guide_with_left_shape"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    gc = rng.randint(4, 5)
    for r in range(h):
        g[r][gc] = 9
    shape = rng.choice([
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ])
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    top = rng.randint(0, h - 4); left = rng.randint(0, gc - 3)
    paint_at(g, top, left, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_guide":
        # missing 9-col → no axis to mirror
        g[2][1] = 4; g[3][2] = 6
        return g
    if name == "no_shape":
        # guide only, no left shape → rule has nothing to mirror
        gc = 5
        for r in range(h):
            g[r][gc] = 9
        return g
    if name == "cells_both_sides":
        # cells on both sides → ambiguous source side
        gc = 5
        for r in range(h):
            g[r][gc] = 9
        g[2][1] = 4; g[3][2] = 4  # left
        g[2][8] = 6; g[4][9] = 6  # right
        return g
    return g
