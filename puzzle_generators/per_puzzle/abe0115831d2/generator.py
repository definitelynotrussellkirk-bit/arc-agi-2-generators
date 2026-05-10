"""Generator for arc_additional_puzzle_bank_volume6:E41 — Recolor smallest 2-blob to 8.

Rule: among all 2-color blobs, find the one with smallest size; paint
its cells 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_smallest, single_blob, no_2_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "abe0115831d2"
VERSION = "1.1.0"
TASK_ID = "abe0115831d2"
SUMMARY = "3-4 disjoint 2-blobs of distinct sizes; the smallest is unique."

INVARIANTS = [
    ">=3 disjoint blobs of color 2",
    "exactly 1 blob has the minimum size",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_smallest", "single_blob", "no_2_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    big = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
    med = [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)]
    small_options = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0)],
        [(0, 0)],
    ]
    sml = rng.choice(small_options)
    placements = [
        (1, 1, big),
        (rng.randint(3, 5), rng.randint(5, 7), med),
        (rng.randint(h - 4, h - 2), rng.randint(0, 2), sml),
    ]
    rng.shuffle(placements)
    for top, left, s in placements:
        paint_at(g, top, left, s, 2)
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "tied_smallest":
        # multiple blobs share the minimum size → "unique smallest" invariant violated, ambiguous
        big = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        small = [(0, 0), (1, 0)]  # size 2
        paint_at(g, 1, 1, big, 2)
        paint_at(g, 5, 4, small, 2)
        paint_at(g, 7, 8, small, 2)
        g[h - 1][w - 1] = 5
        return g
    if name == "single_blob":
        # only one 2-blob → trivially the smallest, rule reduces to "recolor that blob to 8"
        paint_at(g, 3, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        g[h - 1][w - 1] = 5
        return g
    if name == "no_2_blobs":
        # no color-2 cells at all → rule has no targets
        for r, c in [(2, 2), (4, 5), (6, 8)]:
            g[r][c] = 4
        g[h - 1][w - 1] = 5
        return g
    return g
