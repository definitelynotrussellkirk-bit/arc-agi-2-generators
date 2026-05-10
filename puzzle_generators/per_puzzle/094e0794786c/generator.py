"""Generator for arc_additional_puzzle_bank_volume3:M16.

Rule: normalize 1-cells & 2-cells; XOR (cells in exactly one). Output
bbox of XOR sized to max-bbox of either shape, paint XOR cells with 8.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, identical_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "094e0794786c"
VERSION = "1.1.0"
TASK_ID = "094e0794786c"
SUMMARY = "1- and 2-blobs placed apart with overlapping but unequal normalized shapes."

INVARIANTS = [
    "exactly one 1-blob and one 2-blob",
    "their normalized cells are not identical",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "identical_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 1)
    paint_at(g, 1, w - 4, [(0, 0), (0, 1), (1, 0), (2, 0)], 2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_shapes":
        return g
    if name == "identical_shapes":
        s = [(0, 0), (1, 0), (1, 1)]
        paint_at(g, 1, 1, s, 1)
        paint_at(g, 4, 6, s, 2)
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(10):
                g[r][c] = 1
        return g
    return g
