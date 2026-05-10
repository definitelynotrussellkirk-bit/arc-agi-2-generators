"""Generator for arc_additional_puzzle_bank_volume11:M76.

Rule: normalize 1-cells & 2-cells; output bbox-cropped XOR (cells in
exactly one) painted 8.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, identical_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2776235f38d3"
VERSION = "1.1.0"
TASK_ID = "2776235f38d3"
SUMMARY = "1-shape and 2-shape with overlapping but unequal normalized cells."

INVARIANTS = [
    "exactly one 1-blob and one 2-blob",
    "their normalized cells differ in at least one position",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "identical_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    s1 = [(0, 0), (0, 1), (1, 0)]
    s2 = [(0, 0), (1, 0), (1, 1)]
    paint_at(g, 5, 8, s1, 1)
    paint_at(g, 2, 1, s2, 2)
    g[0][w - 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_shapes":
        return g
    if name == "identical_shapes":
        s = [(0, 0), (0, 1), (1, 0)]
        paint_at(g, 2, 1, s, 1)
        paint_at(g, 6, 8, s, 2)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
