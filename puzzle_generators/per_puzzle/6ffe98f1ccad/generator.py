"""Generator for arc_additional_puzzle_bank_volume8:M50.

Rule: dr/dc = (1-marker − 2-marker). Take the largest 4-blob and stamp a
translated copy in color 8 at offset (dr, dc).

Combinatorial axes (9): grid_h/w, palette_kind, marker_offset_r,
marker_offset_c, blob_size, palette_size, position_bias,
n_distinct_colors, texture.
Degenerates: no_blob, no_markers, markers_collide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "6ffe98f1ccad"
VERSION = "1.1.0"
TASK_ID = "6ffe98f1ccad"
SUMMARY = "2-marker, 1-marker (downstream), 4-blob; output translates 4-blob to 8."

INVARIANTS = [
    "exactly one 2-cell, one 1-cell",
    "exactly one 4-blob",
    "translated 4-cells stay in-bounds",
]

PALETTE_KINDS = ("default", "small_blob", "wide_offset", "diagonal_offset")
DEGENERATE_TEXTURES = ("no_blob", "no_markers", "markers_collide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_offset":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "blob_size":      {"type": "int", "default": "5", "valid": "5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "lower_blob",
                       "valid": "lower_blob"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    paint_at(g, h - 4, 0, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)], 4)
    g[h // 2][2] = 2
    g[h // 2 - 2][5] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blob":
        # markers but no 4-blob to translate
        g[h // 2][2] = 2
        g[h // 2 - 2][5] = 1
        return g
    if name == "no_markers":
        # blob but no markers — translation vector undefined
        paint_at(g, h - 4, 0, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)], 4)
        return g
    if name == "markers_collide":
        # 1 and 2 at same cell — zero offset, stamp lands on blob
        paint_at(g, h - 4, 0, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)], 4)
        g[h // 2][3] = 2
        g[h // 2][3] = 1
        return g
    return g
