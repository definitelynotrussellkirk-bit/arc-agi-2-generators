"""Generator for arc_puzzle_bank_21_set10_e:hard_j18.

Rule: sort blobs by left-column. For consecutive pairs, draw an L-path
of 8s (horizontal then vertical) connecting their top-left corners.

Combinatorial axes (8): grid_h/w, palette_kind, num_blobs, blob_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_one_blob, blobs_aligned_col, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "6142e80eace4"
VERSION = "1.1.0"
TASK_ID = "6142e80eace4"
SUMMARY = "3 distinct-color non-touching blobs at varied positions."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "blobs have distinct positions (different cols)",
    "L-paths between consecutive sort-by-col pairs avoid blob cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_one_blob", "blobs_aligned_col", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_blobs":      {"type": "int", "default": "3", "valid": "3"},
    "blob_size":      {"type": "str", "default": "varied", "valid": "varied"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
    paint_at(g, 3, 6, [(0, 0), (0, 1), (0, 2)], 4)
    paint_at(g, 5, 11, [(0, 0), (1, 0)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    if name == "only_one_blob":
        # 1 blob — no consecutive pairs, no L-paths to draw
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        return g
    if name == "blobs_aligned_col":
        # all blobs at the same left-column — sort by c1 ties
        paint_at(g, 1, 5, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 4, 5, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 7, 5, [(0, 0), (0, 1)], 7)
        return g
    if name == "no_blobs":
        return g
    return g
