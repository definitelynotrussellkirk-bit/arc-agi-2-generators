"""Generator for arc_additional_puzzles_21_set17_bundle:E118 — Bbox crop of largest blob.

Rule: among all 4-connected non-bg blobs, find the one with greatest
size; output bbox subgrid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_largest.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2c7b1545edf9"
VERSION = "1.1.0"
TASK_ID = "2c7b1545edf9"
SUMMARY = "3 blobs of distinct sizes; largest is unique."

INVARIANTS = [
    "exactly 3 disjoint blobs",
    "exactly 1 blob has the maximum size",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_largest")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_blobs_distinct_sizes",
                       "valid": "three_blobs_distinct_sizes"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    big = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    med = [(0, 0), (0, 1), (1, 1), (2, 0)]
    sml = [(0, 0), (0, 1)]
    placements = [
        (rng.randint(1, 2), rng.randint(0, 2), big, pal[0]),
        (rng.randint(1, 3), rng.randint(w - 4, w - 3), med, pal[1]),
        (rng.randint(h - 2, h - 1), rng.randint(2, 4), sml, pal[2]),
    ]
    rng.shuffle(placements)
    for top, left, s, color in placements:
        paint_at(g, top, left, s, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blob to crop
        return g
    if name == "single_blob":
        # only one blob → "largest" is trivially identity, no selection signal
        big = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        paint_at(g, 2, 2, big, 4)
        return g
    if name == "tied_largest":
        # two blobs of equal max size → ambiguous "largest"
        big = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        paint_at(g, 1, 0, big, 4)
        paint_at(g, 5, 6, big, 6)
        return g
    return g
