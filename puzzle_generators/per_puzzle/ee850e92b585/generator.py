"""Generator for arc_puzzle_bank_21_set13_bundle:medium_m04 — area rank recolor (asc, from 1).

Rule: sort blobs ascending by area; recolor smallest=1, next=2, etc.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_areas, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ee850e92b585"
VERSION = "1.1.0"
TASK_ID = "ee850e92b585"
SUMMARY = "3 blobs of distinct sizes; ranks start at 1 (smallest) ascending."

INVARIANTS = [
    "background is 0",
    "every blob has a strictly distinct size from every other",
    "input colors aren't already the rank colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_areas", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "distinct_size_blobs_non_rank_colors",
                       "valid": "distinct_size_blobs_non_rank_colors"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = 3
    sizes = rng.sample(range(2, 7), n)
    palette = rng.sample([4, 5, 7, 9], n)
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
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "tied_areas":
        # 3 blobs same size → rank ordering ambiguous (sort key tied)
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4   # size 3
        for (r, c) in [(1, 6), (1, 7), (2, 6)]: g[r][c] = 7   # size 3 (tied)
        for (r, c) in [(6, 3), (6, 4), (7, 3)]: g[r][c] = 9   # size 3 (tied)
        return g
    if name == "single_blob":
        # only 1 blob → trivial ranking, output is just one recoloring to 1
        for (r, c) in [(3, 4), (3, 5), (4, 4), (4, 5)]: g[r][c] = 4
        return g
    if name == "no_blobs":
        # blank → no blobs to rank
        return g
    return g
