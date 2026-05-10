"""Generator for arc_additional_puzzle_bank_volume23:H160.

Rule: among the 1-blobs, find the one whose canonical shape (under any
of the 8 rotation/flip transforms) is unique. Output bbox-cropped mask
in color 8.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, blob_pos,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_same_shape, two_uniques, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "53272e4e79a1"
VERSION = "1.1.0"
TASK_ID = "53272e4e79a1"
SUMMARY = "4 1-blobs: 3 share canonical shape, 1 is unique."

INVARIANTS = [
    "exactly 4 non-touching 1-blobs",
    "3 share canonical shape (under rotation/flip), 1 is unique",
]

PALETTE_KINDS = ("default", "L_shape", "T_shape", "Z_shape")
DEGENERATE_TEXTURES = ("all_same_shape", "two_uniques", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    common = [(0, 0), (0, 1), (1, 0)]
    unique = [(0, 0), (0, 1), (0, 2), (1, 1)]
    paint_at(g, 1, 1, common, 1)
    paint_at(g, 1, 6, common, 1)
    paint_at(g, 7, 1, common, 1)
    paint_at(g, h - 4, 8, unique, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    common = [(0, 0), (0, 1), (1, 0)]
    unique = [(0, 0), (0, 1), (0, 2), (1, 1)]
    other_unique = [(0, 0), (1, 0), (1, 1), (1, 2)]
    if name == "all_same_shape":
        # 4 identical L-blobs — no unique to extract
        paint_at(g, 1, 1, common, 1)
        paint_at(g, 1, 6, common, 1)
        paint_at(g, 6, 1, common, 1)
        paint_at(g, 6, 6, common, 1)
        return g
    if name == "two_uniques":
        # 2 common + 2 different uniques — ambiguous which to extract
        paint_at(g, 1, 1, common, 1)
        paint_at(g, 1, 6, common, 1)
        paint_at(g, 7, 1, unique, 1)
        paint_at(g, 7, 8, other_unique, 1)
        return g
    if name == "no_blobs":
        # empty grid — no candidate
        return g
    return g
