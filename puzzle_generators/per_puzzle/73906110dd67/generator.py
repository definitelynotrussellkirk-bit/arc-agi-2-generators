"""Generator for arc_puzzle_bank_21_more:hard_b01.

Rule: sort objects by size desc; output is vertical stack of their bbox
crops with 1-row gaps; output width = max obj width.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "73906110dd67"
VERSION = "1.1.0"
TASK_ID = "73906110dd67"
SUMMARY = "3 distinct-color blobs of distinct sizes."

INVARIANTS = [
    "exactly 3 non-touching blobs of distinct sizes",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "size_spread":    {"type": "str", "default": "3_4_5", "valid": "3_4_5"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], palette[0])
    paint_at(g, 1, 6, [(0, 0), (1, 0), (2, 0), (2, 1)], palette[1])
    paint_at(g, h - 4, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "equal_sizes":
        # 3 blobs all size 3 → "sort by size" tie-break is fragile
        sq = [(0, 0), (0, 1), (1, 0)]
        paint_at(g, 1, 1, sq, 4)
        paint_at(g, 1, 6, sq, 6)
        paint_at(g, h - 4, 3, sq, 7)
        return g
    if name == "single_blob":
        # 1 blob → vertical stack is just the blob crop, no rule effect visible
        paint_at(g, 3, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 4)
        return g
    if name == "no_blobs":
        # empty grid — nothing to stack
        return g
    return g
