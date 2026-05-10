"""Generator for arc_puzzle_bank_21_set10_e:hard_j16.

Rule: each object → cropped subgrid; output cell (r,c) = 8 if ≥2 objects
have non-zero at (r,c); crop to content.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_overlap, single_object, all_three_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "15df00eb9323"
VERSION = "1.1.0"
TASK_ID = "15df00eb9323"
SUMMARY = "3 small distinct-color blobs of similar size; their cropped overlay has overlap cells."

INVARIANTS = [
    "exactly 3 non-touching blobs of similar size (3-4 cells each)",
    "blobs use distinct colors",
    "cropped overlay has at least one cell where ≥2 blobs are non-zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_overlap", "single_object", "all_three_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "horizontal_three",
                       "valid": "horizontal_three"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    s1 = [(0, 0), (0, 1), (1, 1), (2, 1)]
    s2 = [(0, 0), (0, 1), (0, 2), (1, 1)]
    s3 = [(0, 0), (1, 0), (1, 1), (2, 0)]
    paint_at(g, 1, 1, s1, palette[0])
    paint_at(g, 1, 5, s2, palette[1])
    paint_at(g, 1, 9, s3, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 13
    g = full_grid(h, w, 0)
    if name == "no_overlap":
        # all 3 normalized shapes pairwise disjoint → no ≥2 cell, output empty
        s1 = [(0, 0), (1, 0)]
        s2 = [(0, 1), (1, 1)]
        s3 = [(2, 0), (2, 1)]
        paint_at(g, 1, 1, s1, 4)
        paint_at(g, 1, 5, s2, 6)
        paint_at(g, 1, 9, s3, 7)
        return g
    if name == "single_object":
        # one blob → no pair to overlap with
        paint_at(g, 2, 4, [(0, 0), (0, 1), (1, 0)], 4)
        return g
    if name == "all_three_overlap":
        # all 3 normalized shapes identical → every cell in 3, output uniform 8 (saturated)
        common = [(0, 0), (1, 0), (1, 1)]
        paint_at(g, 1, 1, common, 4)
        paint_at(g, 1, 5, common, 6)
        paint_at(g, 1, 9, common, 7)
        return g
    return g
