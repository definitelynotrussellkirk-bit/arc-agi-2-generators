"""Generator for arc_additional_puzzles_21_set9:E63.

Rule: among all non-bg blobs, find the one with the largest size;
output bbox subgrid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "21345a6ebb11"
VERSION = "1.1.0"
TASK_ID = "21345a6ebb11"
SUMMARY = "2-3 blobs of distinct sizes; largest is unique."

INVARIANTS = [
    "≥2 disjoint blobs",
    "exactly 1 has the maximum size",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    big = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]
    sml = [(0, 0), (1, 0)]
    placements = [
        (rng.randint(1, 2), rng.randint(0, 2), big, pal[0]),
        (rng.randint(h - 3, h - 2), rng.randint(w - 3, w - 2), sml, pal[1]),
    ]
    rng.shuffle(placements)
    for top, left, s, color in placements:
        paint_at(g, top, left, s, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    sml = [(0, 0), (1, 0)]
    if name == "equal_sizes":
        # all blobs share one size → "largest" is ambiguous, tie-break needed
        paint_at(g, 1, 1, sml, 3)
        paint_at(g, 1, w - 3, sml, 5)
        paint_at(g, h - 3, w // 2, sml, 7)
        return g
    if name == "single_blob":
        # only 1 blob → "largest" is trivially the only blob, rule reduces to bbox crop
        big = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]
        paint_at(g, 2, 3, big, 4)
        return g
    if name == "no_blobs":
        # empty grid → no blobs to compare or crop
        return g
    return g
