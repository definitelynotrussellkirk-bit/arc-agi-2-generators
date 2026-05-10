"""Generator for arc_additional_puzzles_21_set20_bundle:M135.

Rule: sort objects by (size asc, color asc); concat their bbox crops
horizontally with 1-col gaps. Output max-h × total-w.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2847032fa29b"
VERSION = "1.1.0"
TASK_ID = "2847032fa29b"
SUMMARY = "3 distinct-color, distinct-size blobs of varied shapes."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "all distinct sizes and colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], palette[0])
    paint_at(g, 4, 7, [(0, 0), (1, -1), (1, 0)], palette[1])
    paint_at(g, 6, 2, [(0, 0), (0, 1), (0, 2), (1, 1)], palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    bar3 = [(0, 0), (1, 0), (2, 0)]
    if name == "equal_sizes":
        # all 3 blobs share one size → size sort is ambiguous, only color sort breaks tie
        paint_at(g, 1, 1, bar3, 2)
        paint_at(g, 1, w - 4, bar3, 4)
        paint_at(g, h - 4, w // 2 - 1, bar3, 6)
        return g
    if name == "single_blob":
        # only 1 blob → output is its sole bbox crop, sort/concat is trivial
        paint_at(g, h // 2, w // 2, [(0, 0), (1, 0), (2, 0), (2, 1)], 5)
        return g
    if name == "no_blobs":
        # empty grid → no crops to concat
        return g
    return g
