"""Generator for arc_puzzle_bank_21_set7_s:S7_M3 — height-sorted palette row.

Rule: output 1xN with blob colors sorted by descending bbox-height.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_heights, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "4c04ce6c5477"
VERSION = "1.1.0"
TASK_ID = "4c04ce6c5477"
SUMMARY = "3 distinct-color blobs of strictly distinct bbox heights."

INVARIANTS = [
    "background is 0",
    "3 distinct-color blobs",
    "all 3 have strictly distinct bbox heights",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_heights", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "distinct_height_blobs",
                       "valid": "distinct_height_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    sizes = [3, 4, 5]
    used: set[tuple[int, int]] = set()
    placed_heights: set[int] = set()
    for size, color in zip(sizes, palette):
        for _ in range(60):
            cells = grow_blob(rng, h, w, used, size, max_attempts=20)
            if cells is None:
                continue
            rs = [r for r, _ in cells]
            bb_h = max(rs) - min(rs) + 1
            if bb_h in placed_heights:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            placed_heights.add(bb_h)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "tied_heights":
        # all blobs share the same bbox height → sort key is degenerate
        for (r, c) in [(1, 1), (2, 1)]: g[r][c] = 4  # height 2
        for (r, c) in [(1, 5), (2, 5)]: g[r][c] = 6  # height 2
        for (r, c) in [(1, 9), (2, 9)]: g[r][c] = 3  # height 2
        return g
    if name == "single_blob":
        # only one blob → output is single cell, weakly tests sort
        for (r, c) in [(2, 3), (3, 3), (4, 3)]: g[r][c] = 4
        return g
    if name == "no_blobs":
        # blank → no blobs, output empty
        return g
    return g
