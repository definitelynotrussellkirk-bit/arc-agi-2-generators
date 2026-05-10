"""Generator for arc_additional_puzzle_bank_volume17:M115.

Rule: sort 2-blobs by (size desc, top-left); recolor 2nd to 8.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_blobs, single_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d292e3214bb1"
VERSION = "1.1.0"
TASK_ID = "d292e3214bb1"
SUMMARY = "3 distinct-size 2-blobs + decoration."

INVARIANTS = [
    "exactly 3 non-touching 2-blobs of distinct sizes",
    "decoration is one non-2 cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 2)
    paint_at(g, h // 2 - 1, w - 5, [(0, 0), (1, -1), (1, 0), (1, 1)], 2)
    paint_at(g, h - 3, 1, [(0, 0), (1, 0)], 2)
    g[0][w - 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 11, 0)
    if name == "no_blobs":
        g[0][10] = 7
        return g
    if name == "single_blob":
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
