"""Generator for arc_additional_puzzles_21_set15_bundle:M104 — Rank-th object crop.

Rule: rank = at(0,0). Sort objects by (size desc, c1 asc, color asc);
pick rank-th (1-indexed); output bbox crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rank, no_objects, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "27f5eba1051c"
VERSION = "1.1.0"
TASK_ID = "27f5eba1051c"
SUMMARY = "Rank cell at (0,0) (1..3) + 3 distinct-color, distinct-size blobs."

INVARIANTS = [
    "rank at (0,0) ∈ 1..3",
    "exactly 3 non-touching blobs of distinct sizes",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rank", "no_objects", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "rank_with_three_blobs",
                       "valid": "rank_with_three_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        w = ctx.draw_int("grid_w", 12, 13)
        rank = ctx.draw_int("rank", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
        rank = ctx.draw_int("rank", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 12, 14)
        rank = ctx.draw_int("rank", 1, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = rank
    palette = [c for c in range(2, 10) if c != rank]
    rng.shuffle(palette); colors = palette[:3]
    paint_at(g, 2, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], colors[0])  # size 5
    paint_at(g, 2, w - 4, [(0, 0), (0, 1), (1, 0)], colors[1])  # size 3
    paint_at(g, h - 3, w // 2 - 1, [(0, 0), (0, 1)], colors[2])  # size 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_rank":
        # blobs but no rank cell at (0,0) → no selector
        paint_at(g, 2, 1, [(0, 0), (1, 0), (2, 0)], 4)
        paint_at(g, 5, 7, [(0, 0), (0, 1)], 6)
        return g
    if name == "no_objects":
        # rank specified but no body blobs → nothing to pick from
        g[0][0] = 2
        return g
    if name == "tied_sizes":
        # all blobs equal size → ambiguous "size desc" rank
        g[0][0] = 2
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 2, w - 4, [(0, 0), (0, 1), (1, 0)], 6)
        paint_at(g, h - 3, 5, [(0, 0), (0, 1), (1, 0)], 7)
        return g
    return g
