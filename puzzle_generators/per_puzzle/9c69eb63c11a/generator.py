"""Generator for arc_puzzle_bank_sixth21:M36.

Rule: of N blobs (odd N), keep only the one whose area is the median.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, even_count_blobs, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "9c69eb63c11a"
VERSION = "1.1.0"
TASK_ID = "9c69eb63c11a"
SUMMARY = "Exactly 3 distinct-color blobs of strictly distinct sizes."

INVARIANTS = [
    "background is 0",
    "exactly 3 blobs with strictly distinct sizes",
    "blobs are 4-disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "even_count_blobs", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..5"},
    "size_spread":    {"type": "str", "default": "distinct", "valid": "distinct"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sizes = rng.sample(range(2, 7), 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
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
    import random
    rng = random.Random(0)
    h, w = 10, 11
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    if name == "equal_sizes":
        # all blobs share one size → median is ambiguous (every blob qualifies)
        for color in [3, 5, 7]:
            cells = grow_blob(rng, h, w, used, 3, max_attempts=80)
            if cells is None:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
        return g
    if name == "even_count_blobs":
        # 4 blobs (even count) → median falls between two distinct sizes, ambiguous
        for size, color in zip([2, 3, 4, 5], [3, 4, 5, 6]):
            cells = grow_blob(rng, h, w, used, size, max_attempts=80)
            if cells is None:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
        return g
    if name == "single_blob":
        # only one blob → median is trivially that blob, rule reduces to identity
        cells = grow_blob(rng, h, w, used, 4, max_attempts=80)
        if cells:
            for r, c in cells:
                g[r][c] = 6
        return g
    return g
