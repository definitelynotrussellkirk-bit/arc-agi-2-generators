"""Generator for arc_additional_puzzles_21_set12_bundle:H83.

Rule: sort objects by (color, r1, c1); n×n matrix: 1 if size[r] < size[c],
2 if equal, 3 if greater.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "bdba622b3265"
VERSION = "1.1.0"
TASK_ID = "bdba622b3265"
SUMMARY = "4 distinct-color blobs of varied sizes."

INVARIANTS = [
    "exactly 4 non-touching distinct-color blobs",
    "at least 2 distinct sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "size_spread":    {"type": "str", "default": "varied", "valid": "varied"},
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
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(2, 10)); rng.shuffle(colors)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2)], colors[0])
    paint_at(g, 1, w - 5, [(0, 0), (0, 1), (0, 2), (1, 1)], colors[1])
    paint_at(g, h - 6, 1, [(0, 0), (1, 0)], colors[2])
    paint_at(g, h - 4, w - 5, [(0, 0), (1, 0), (2, 0), (2, 1)], colors[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "equal_sizes":
        # all blobs share one size → matrix is uniformly 2 (equal everywhere)
        single = [(0, 0), (0, 1), (1, 0)]
        paint_at(g, 1, 1, single, 2)
        paint_at(g, 1, w - 4, single, 3)
        paint_at(g, h - 4, 1, single, 4)
        paint_at(g, h - 4, w - 4, single, 5)
        return g
    if name == "single_blob":
        # only 1 blob → matrix is 1×1 (just self-comparison)
        paint_at(g, h // 2, w // 2, [(0, 0), (0, 1), (1, 0), (1, 1)], 5)
        return g
    if name == "no_blobs":
        # empty grid → matrix is 0×0, no comparisons to make
        return g
    return g
