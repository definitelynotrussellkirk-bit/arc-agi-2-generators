"""Generator for arc_additional_puzzles_21_set18_bundle:M123.

Rule: sort objects by (color asc, size asc); n×n matrix: cell (r,c) =
color of larger of objs[r] / objs[c] (size); 0 if r==c or sizes equal.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_blob, four_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "df0d6baae973"
VERSION = "1.1.0"
TASK_ID = "df0d6baae973"
SUMMARY = "3 distinct-color, distinct-size blobs."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "all distinct colors and distinct sizes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_blob", "four_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "size_spread":    {"type": "str", "default": "2_3_4", "valid": "2_3_4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(2, 10)); rng.shuffle(colors)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], colors[0])
    paint_at(g, 1, w - 5, [(0, 0), (0, 1), (1, 0)], colors[1])
    paint_at(g, h - 4, 1, [(0, 0), (1, 0)], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "equal_sizes":
        # 3 blobs but all the same size → "larger" is undefined for every pair
        sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
        paint_at(g, 1, 1, sq, 4)
        paint_at(g, 1, w - 5, sq, 6)
        paint_at(g, h - 4, 1, sq, 7)
        return g
    if name == "single_blob":
        # only 1 blob → matrix is 1×1; predicate "exactly 3 blobs" fails
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        return g
    if name == "four_blobs":
        # 4 blobs → matrix would be 4×4; predicate "exactly 3 blobs" fails
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        paint_at(g, 1, w - 5, [(0, 0), (0, 1), (1, 0)], 6)
        paint_at(g, h - 4, 1, [(0, 0), (1, 0)], 7)
        paint_at(g, h - 3, w - 3, [(0, 0)], 9)
        return g
    return g
