"""Generator for arc_puzzle_bank_eighth21:M50 — keep largest blob per color.

Rule: for each color, keep only the largest blob; drop other (smaller)
blobs of the same color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_per_color, single_blob_per_color, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "666934e5ac80"
VERSION = "1.1.0"
TASK_ID = "666934e5ac80"
SUMMARY = "Each of 2 colors has a clearly-large blob + a strictly-smaller blob."

INVARIANTS = [
    "background is 0",
    "exactly 2 colors used",
    "each color has 2 blobs of strictly distinct sizes (large + small)",
    "blobs (across colors) don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_per_color", "single_blob_per_color", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "large_plus_small_per_color",
                       "valid": "large_plus_small_per_color"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    used: set[tuple[int, int]] = set()
    for color in palette:
        cells = grow_blob(rng, h, w, used, 4, max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
        cells = grow_blob(rng, h, w, used, rng.randint(1, 2), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "tied_per_color":
        # both blobs of each color have equal size → "largest" ambiguous
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4   # size 3
        for (r, c) in [(5, 1), (5, 2), (6, 2)]: g[r][c] = 4   # also size 3
        for (r, c) in [(1, 8), (1, 9)]: g[r][c] = 6   # size 2
        for (r, c) in [(7, 8), (7, 9)]: g[r][c] = 6   # also size 2
        return g
    if name == "single_blob_per_color":
        # each color has only one blob → trivially largest, rule is identity
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for (r, c) in [(5, 8), (5, 9), (6, 8), (6, 9)]: g[r][c] = 6
        return g
    if name == "no_blobs":
        # blank grid → rule has nothing to filter
        return g
    return g
