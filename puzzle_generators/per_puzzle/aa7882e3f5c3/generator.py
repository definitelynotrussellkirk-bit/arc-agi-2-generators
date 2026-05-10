"""Generator for arc_additional_puzzles_21_set21_bundle:M146 — Pairwise size-comparison matrix.

Rule: sort objects by obj-c1; output is N×N grid where (r, c) is:
  2 if r == c
  5 if size[r] > size[c]
  0 otherwise

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "aa7882e3f5c3"
VERSION = "1.1.0"
TASK_ID = "aa7882e3f5c3"
SUMMARY = "N non-touching blobs of distinct sizes; output is NxN size-comparison matrix."

INVARIANTS = [
    "exactly 2..4 blobs",
    "all distinct sizes",
    "blobs spaced left-to-right (so sort-by-c1 is unambiguous)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9",   "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..4",   "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4",   "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_to_right_band",
                       "valid": "left_to_right_band"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 12, 14)
        n_blobs = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 16, 18)
        n_blobs = ctx.draw_int("n_blobs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 12, 18)
        n_blobs = ctx.draw_int("n_blobs", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = list(range(2, 8)); rng.shuffle(sizes)
    sizes = sizes[:n_blobs]
    colors = list(range(1, 10)); rng.shuffle(colors)
    used = set()
    cur_c = 1
    for i, size in enumerate(sizes):
        for _ in range(15):
            if cur_c >= w - 2: break
            placed = False
            for _ in range(10):
                blob = grow_blob(rng, h, min(w, cur_c + 4), used, size)
                if blob is None: continue
                cs = [c for _, c in blob]
                if min(cs) < cur_c - 1: continue
                used |= blob
                for r, c in blob: g[r][c] = colors[i % len(colors)]
                cur_c = max(cs) + 2
                placed = True
                break
            if placed: break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 14
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # all blobs same size → comparison matrix has no 5s, only 2s on diagonal
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for (r, c) in [(1, 6), (1, 7), (2, 7)]: g[r][c] = 6
        for (r, c) in [(4, 10), (5, 10), (5, 11)]: g[r][c] = 3
        return g
    if name == "single_blob":
        # only one blob → 1x1 output, just a 2 cell
        for (r, c) in [(2, 5), (2, 6), (3, 5), (3, 6)]: g[r][c] = 4
        return g
    if name == "no_blobs":
        # blank grid → no objects to compare, output is empty/undefined
        return g
    return g
