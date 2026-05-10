"""Generator for arc_additional_puzzle_bank_volume19:H133.

Rule: 3 present → intersection; 4 present → union; else XOR. Output
bbox-cropped result in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ctrl,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_overlap, missing_shape, both_ctrls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import L_TROMINO_SE

GENERATOR_ID = "56e5ade4e829"
VERSION = "1.1.0"
TASK_ID = "56e5ade4e829"
SUMMARY = "1-shape, 2-shape, and ctrl marker (3 or 4 or neither) + decoration."

INVARIANTS = [
    "exactly one 1-blob and one 2-blob",
    "ctrl is exactly one of: 3 cell, 4 cell, or neither",
    "shapes overlap in some normalized cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_overlap", "missing_shape", "both_ctrls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ctrl":           {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "two_shapes_corner_ctrl",
                       "valid": "two_shapes_corner_ctrl"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 11, 11)
        ctrl = ctx.draw_int("ctrl", 0, 0)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        ctrl = ctx.draw_int("ctrl", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        ctrl = ctx.draw_int("ctrl", 0, 2)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, L_TROMINO_SE, 1)
    paint_at(g, 1, w - 4, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 2)
    if ctrl == 1: g[h - 1][0] = 3
    elif ctrl == 2: g[h - 1][0] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_overlap":
        # 1- and 2- shapes share no normalized cells → intersection empty, XOR=union
        paint_at(g, 1, 1, [(0, 0), (1, 0)], 1)
        paint_at(g, 1, 8, [(0, 1), (1, 1)], 2)
        return g
    if name == "missing_shape":
        # only 1-shape, no 2-shape → set op undefined
        paint_at(g, 1, 1, L_TROMINO_SE, 1)
        g[h - 1][0] = 3
        return g
    if name == "both_ctrls":
        # both 3 and 4 markers present → ambiguous which set op to apply
        paint_at(g, 1, 1, L_TROMINO_SE, 1)
        paint_at(g, 1, w - 4, [(0, 0), (1, 0), (2, 0)], 2)
        g[h - 1][0] = 3
        g[h - 1][w - 1] = 4
        return g
    return g
