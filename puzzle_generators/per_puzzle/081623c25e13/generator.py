"""Generator for arc_additional_puzzle_bank_volume3:H19 — Crop n-th largest.

Rule: n = at(0,0); set (0,0)=0; sort objs by (size desc, r1, c1); take
n-th object; output bbox-cropped normalized cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_n, n_out_of_range, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "081623c25e13"
VERSION = "1.1.0"
TASK_ID = "081623c25e13"
SUMMARY = "n at (0,0) ∈ 1..3 + 3 distinct-color, distinct-size blobs."

INVARIANTS = [
    "n at (0,0) ∈ 1..3",
    "exactly 3 non-touching blobs of distinct sizes and distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_n", "n_out_of_range", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n":              {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "n_at_origin_3_distinct_blobs",
                       "valid": "n_at_origin_3_distinct_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..4"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 10, 12)
        n = ctx.draw_int("n", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = n
    palette = [c for c in range(2, 10) if c != n]
    rng.shuffle(palette)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], palette[0])  # size 4
    paint_at(g, h - 3, 2, [(0, 0), (0, 1)], palette[1])  # size 2
    paint_at(g, 4, w - 4, [(0, 0), (1, 0), (2, 0)], palette[2])  # size 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_n":
        # (0,0) is 0 → no n value to look up, rule has no rank index
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        paint_at(g, h - 3, 2, [(0, 0), (0, 1)], 6)
        paint_at(g, 4, w - 4, [(0, 0), (1, 0), (2, 0)], 3)
        return g
    if name == "n_out_of_range":
        # n=5 but only 3 blobs → rank index out of range, lookup fails
        g[0][0] = 5
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        paint_at(g, h - 3, 2, [(0, 0), (0, 1)], 6)
        paint_at(g, 4, w - 4, [(0, 0), (1, 0), (2, 0)], 3)
        return g
    if name == "tied_sizes":
        # 3 blobs all same size → "n-th largest" ambiguous (sort key tied)
        g[0][0] = 2
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 4)   # size 3
        paint_at(g, h - 3, 2, [(0, 0), (1, 0), (1, 1)], 6)   # size 3 (tied)
        paint_at(g, 4, w - 4, [(0, 0), (0, 1), (1, 1)], 3)   # size 3 (tied)
        return g
    return g
