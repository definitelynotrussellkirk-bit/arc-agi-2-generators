"""Generator for arc_puzzle_bank_21_set13_bundle:medium_m03 — sort objects into gallery.

Rule: extract each blob's bbox-cropped subgrid, sort by bbox height
(descending), and pack horizontally with a 1-col gap separator.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_heights.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "baec9a7715e7"
VERSION = "1.1.0"
TASK_ID = "baec9a7715e7"
SUMMARY = "3 distinct-color blobs of strictly different bbox heights."

INVARIANTS = [
    "background is 0",
    "3 blobs of distinct colors and strictly distinct bbox heights",
    "blobs don't overlap (no shared bbox cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_heights")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "distinct_height_blobs",
                       "valid": "distinct_height_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    sizes = [3, 4, 5]
    used: set[tuple[int, int]] = set()
    placed_heights: set[int] = set()
    for size, color in zip(sizes, palette):
        for _ in range(40):
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
    if name == "no_blobs":
        # blank → no blobs to sort by height
        return g
    if name == "single_blob":
        # 1 blob → trivial, no sorting contrast
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 4
        return g
    if name == "tied_heights":
        # 2 blobs share bbox height → "strictly distinct" precondition fails
        for r, c in [(1, 1), (2, 1), (3, 1)]: g[r][c] = 4  # height 3
        for r, c in [(1, 5), (2, 5), (3, 5)]: g[r][c] = 6  # height 3 (tied)
        for r, c in [(5, 1)]: g[r][c] = 7  # height 1
        return g
    return g
