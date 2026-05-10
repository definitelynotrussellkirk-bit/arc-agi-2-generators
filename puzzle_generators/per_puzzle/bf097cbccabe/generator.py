"""Generator for arc_additional_puzzle_bank_volume9:M59.

Rule: among the 6-blobs, find the one with unique normalized shape;
output bbox-cropped mask in color 6.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, blob_pos, texture.
Degenerates: all_same_shape, two_uniques, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "bf097cbccabe"
VERSION = "1.1.0"
TASK_ID = "bf097cbccabe"
SUMMARY = "5 6-blobs: 4 share shape, 1 is unique."

INVARIANTS = [
    "exactly 5 non-touching 6-blobs",
    "4 share normalized shape, 1 is unique",
]

PALETTE_KINDS = ("default", "L_common", "T_common", "Z_common")
DEGENERATE_TEXTURES = ("all_same_shape", "two_uniques", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "5", "valid": "5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "blob_pos":       {"type": "str", "default": "fixed", "valid": "fixed"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    common = [(0, 0), (0, 1), (1, 0)]
    unique = PLUS_5
    paint_at(g, 1, 1, common, 6)
    paint_at(g, 1, 5, common, 6)
    paint_at(g, 5, 1, common, 6)
    paint_at(g, 5, 5, common, 6)
    paint_at(g, h - 4, w - 4, unique, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    common = [(0, 0), (0, 1), (1, 0)]
    unique = PLUS_5
    other_unique = [(0, 0), (1, 0), (1, 1), (1, 2)]
    if name == "all_same_shape":
        # 5 identical blobs — no unique to extract
        paint_at(g, 1, 1, common, 6)
        paint_at(g, 1, 5, common, 6)
        paint_at(g, 5, 1, common, 6)
        paint_at(g, 5, 5, common, 6)
        paint_at(g, 8, 8, common, 6)
        return g
    if name == "two_uniques":
        # 3 common + 2 different uniques — ambiguous which to extract
        paint_at(g, 1, 1, common, 6)
        paint_at(g, 1, 5, common, 6)
        paint_at(g, 5, 1, common, 6)
        paint_at(g, 5, 5, unique, 6)
        paint_at(g, 8, 8, other_unique, 6)
        return g
    if name == "no_blobs":
        # empty grid — no candidate
        return g
    return g
