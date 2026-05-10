"""Generator for arc_additional_puzzles_21_set9:M59 — Pick k-th object by sort and crop.

Rule: k = at(0,0); set (0,0)=0; sort objs by (size asc, color asc, r1, c1);
take (k-1)-th; output bbox crop from original grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, k,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_k, k_out_of_range, tied_sort_keys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "3731418cffe2"
VERSION = "1.1.0"
TASK_ID = "3731418cffe2"
SUMMARY = "k at (0,0) ∈ 1..3 + 3 distinct-size, distinct-color blobs."

INVARIANTS = [
    "k at (0,0) ∈ 1..3",
    "exactly 3 non-touching blobs of distinct sizes and distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_k", "k_out_of_range", "tied_sort_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "k":              {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "k_at_origin_3_distinct_blobs",
                       "valid": "k_at_origin_3_distinct_blobs"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        k = ctx.draw_int("k", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        k = ctx.draw_int("k", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
        k = ctx.draw_int("k", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = k
    palette = [c for c in range(2, 10) if c != k]
    rng.shuffle(palette)
    paint_at(g, 1, 2, [(0, 0), (0, 1)], palette[0])  # size 2
    paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 0)], palette[1])  # size 3
    paint_at(g, 6, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1)], palette[2])  # size 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_k":
        # (0,0) is 0 → no k value, rule has no rank index
        paint_at(g, 1, 2, [(0, 0), (0, 1)], 4)
        paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 0)], 6)
        paint_at(g, 6, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1)], 3)
        return g
    if name == "k_out_of_range":
        # k = 5 but only 3 blobs → rank index out of range
        g[0][0] = 5
        paint_at(g, 1, 2, [(0, 0), (0, 1)], 4)
        paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 0)], 6)
        paint_at(g, 6, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1)], 3)
        return g
    if name == "tied_sort_keys":
        # 3 blobs all same (size, color) → sort key fully tied → ambiguous selection
        g[0][0] = 2
        paint_at(g, 1, 2, [(0, 0), (0, 1)], 4)
        paint_at(g, 4, 1, [(0, 0), (0, 1)], 4)   # same size, same color
        paint_at(g, 6, w - 4, [(0, 0), (0, 1)], 4)
        return g
    return g
