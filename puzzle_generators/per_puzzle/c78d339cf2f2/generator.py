"""Generator for 19b:m132 — recolor components by perimeter rank.

Rule: sort blobs by bbox perimeter, recolor by rank palette.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_perimeters.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "c78d339cf2f2"
VERSION = "1.1.0"
TASK_ID = "c78d339cf2f2"
SUMMARY = "3 distinct-color blobs of strictly distinct bbox perimeters."

INVARIANTS = [
    "background is 0",
    "3 distinct-color blobs with strictly distinct bbox perimeters",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_perimeters")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "distinct_perim_blobs",
                       "valid": "distinct_perim_blobs"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    used: set[tuple[int, int]] = set()
    seen_perim: set[int] = set()
    for color in palette:
        for _ in range(60):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 5), max_attempts=20)
            if cells is None:
                continue
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            perim = 2 * ((max(rs) - min(rs) + 1) + (max(cs) - min(cs) + 1))
            if perim in seen_perim:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            seen_perim.add(perim)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to rank by perimeter
        return g
    if name == "single_blob":
        # 1 blob → trivial rank, no recoloring contrast
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 4
        return g
    if name == "tied_perimeters":
        # 2 blobs share perimeter → "strictly distinct" precondition fails
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4  # 2x2 bbox
        for r, c in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6  # 2x2 bbox (tied)
        for r, c in [(7, 0), (7, 1), (7, 2), (7, 3)]: g[r][c] = 7  # 1x4 bbox
        return g
    return g
