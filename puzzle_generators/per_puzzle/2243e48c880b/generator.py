"""Generator for arc_puzzle_bank_21_more:medium_b05 — Recolor 3 objects by ascending size.

Rule: sort objects by size ascending. The smallest gets color 2, the
middle gets 4, the largest gets 8. Output is on an empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_blob, two_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "2243e48c880b"
VERSION = "1.1.0"
TASK_ID = "2243e48c880b"
SUMMARY = "Exactly 3 non-touching blobs of distinct sizes; output recolors smallest/middle/largest as 2/4/8."

INVARIANTS = ["exactly 3 components, each with a UNIQUE size"]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_blob", "two_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread_distinct_sizes",
                       "valid": "spread_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = list(range(2, 7))
    rng.shuffle(sizes)
    sizes = sorted(sizes[:3])
    colors = list(range(1, 10))
    rng.shuffle(colors)
    used = set()
    for i, size in enumerate(sizes):
        blob = grow_blob(rng, h, w, used, size)
        if blob is None: continue
        used |= blob
        for r, c in blob: g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # 3 blobs share the same size → smallest/middle/largest ordering ambiguous
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4   # size 3
        for (r, c) in [(1, 5), (1, 6), (2, 6)]: g[r][c] = 6   # size 3
        for (r, c) in [(5, 2), (5, 3), (6, 2)]: g[r][c] = 8   # size 3
        return g
    if name == "single_blob":
        # one blob → no smaller/middle/largest comparison
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4)]: g[r][c] = 4
        return g
    if name == "two_blobs":
        # two blobs → rule expects exactly 3, predicate fails
        for (r, c) in [(1, 1), (1, 2)]: g[r][c] = 4
        for (r, c) in [(5, 5), (5, 6), (6, 5), (6, 6)]: g[r][c] = 6
        return g
    return g
