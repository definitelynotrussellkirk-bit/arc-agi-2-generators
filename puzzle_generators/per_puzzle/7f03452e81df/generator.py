"""Generator for arc_additional_puzzles_21_set2:M8 — Crop to smallest object.

Rule: pick first object after sorting by (size asc, r1 asc, c1 asc); crop
grid to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_smallest.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "7f03452e81df"
VERSION = "1.1.0"
TASK_ID = "7f03452e81df"
SUMMARY = "Several non-touching blobs of distinct sizes; output crops to smallest's bbox."

INVARIANTS = [
    "between 2 and 4 non-touching blobs",
    "all distinct sizes",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_smallest")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "spaced_blobs_distinct_sizes",
                       "valid": "spaced_blobs_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        n_blobs = ctx.draw_int("n_blobs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        n_blobs = ctx.draw_int("n_blobs", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = list(range(2, 8)); rng.shuffle(sizes); sizes = sorted(sizes[:n_blobs])
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    for i, sz in enumerate(sizes):
        for _ in range(20):
            blob = grow_blob(rng, h, w, used, sz)
            if blob is None or len(blob) != sz: continue
            used |= blob
            for r, c in blob: g[r][c] = colors[i]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blob to crop to
        return g
    if name == "single_blob":
        # only one blob → "smallest" trivially identity (no contrast)
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        return g
    if name == "tied_smallest":
        # two blobs of equal smallest size → ambiguous "smallest"
        g[1][1] = 4; g[1][2] = 4   # size 2
        g[6][7] = 6; g[6][8] = 6   # size 2 (tied)
        for r, c in [(4, 4), (4, 5), (5, 4), (5, 5)]: g[r][c] = 7   # size 4
        return g
    return g
