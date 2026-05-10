"""Generator for arc_additional_puzzle_bank_volume10:H68.

Rule: among blue (color-1) objects, the only normalized shape class
that appears once is scaled by two and rendered cyan.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, blob_pos, texture.
Degenerates: all_same_shape, all_unique, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "4a1513fe3fe9"
VERSION = "1.1.0"
TASK_ID = "4a1513fe3fe9"
SUMMARY = "Among blue objects, the only normalized shape class that appears once is scaled by two and rendered cyan."

INVARIANTS = [
    "only color-1 objects are considered",
    "one blue shape class appears exactly once",
    "another blue shape class appears multiple times",
    "the unique class has a nontrivial shape to upscale",
]

PALETTE_KINDS = ("default", "L_repeated", "T_repeated", "Z_repeated")
DEGENERATE_TEXTURES = ("all_same_shape", "all_unique", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "4"},
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 13, 18)
    g = full_grid(h, w, 0)
    repeated = [(0, 0), (1, 0), (1, 1)]
    unique = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, 1, 1, repeated, 1)
    paint_at(g, 1, w - 4, repeated, 1)
    paint_at(g, h - 5, 2, repeated, 1)
    paint_at(g, h - 5, w - 5, unique, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    common = [(0, 0), (1, 0), (1, 1)]
    other_a = [(0, 0), (0, 1), (1, 1), (2, 1)]
    other_b = [(0, 0), (1, 0), (1, 1), (1, 2)]
    if name == "all_same_shape":
        # all 4 blobs share normalized shape — no unique to upscale
        paint_at(g, 1, 1, common, 1)
        paint_at(g, 1, w - 4, common, 1)
        paint_at(g, h - 5, 2, common, 1)
        paint_at(g, h - 5, w - 5, common, 1)
        return g
    if name == "all_unique":
        # every blob a different shape — none is "the only" unique → ambiguous
        paint_at(g, 1, 1, [(0, 0), (1, 0)], 1)
        paint_at(g, 1, w - 4, common, 1)
        paint_at(g, h - 5, 2, other_a, 1)
        paint_at(g, h - 5, w - 5, other_b, 1)
        return g
    if name == "no_blobs":
        # no color-1 blobs — rule has nothing to consider
        return g
    return g
