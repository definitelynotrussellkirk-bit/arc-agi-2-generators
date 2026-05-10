"""Generator for 16b:m109 — recolor by area rank.

Rule: sort blobs by area asc, recolor by rank palette.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, fewer_blobs, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "8a2e39528187"
VERSION = "1.1.0"
TASK_ID = "8a2e39528187"
SUMMARY = "4 distinct-color blobs of strictly distinct sizes."

INVARIANTS = [
    "background is 0",
    "4 distinct-color blobs with strictly distinct sizes",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "fewer_blobs", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "non_touching",
                       "valid": "non_touching"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = rng.sample(range(2, 7), 4)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    used: set[tuple[int, int]] = set()
    for size, color in zip(sizes, palette):
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # two blobs share size → rank tie, mapping ambiguous
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 3
        for r, c in [(4, 5), (4, 6)]: g[r][c] = 5
        for r, c in [(6, 1), (6, 2), (7, 1)]: g[r][c] = 7
        for r, c in [(8, 7), (8, 8)]: g[r][c] = 8
        return g
    if name == "fewer_blobs":
        # only 2 blobs → rank palette has 4 entries but only 2 available
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 3
        for r, c in [(7, 7), (7, 8), (8, 7), (8, 8)]: g[r][c] = 5
        return g
    if name == "no_blobs":
        # empty grid → no blobs to recolor
        return g
    return g
