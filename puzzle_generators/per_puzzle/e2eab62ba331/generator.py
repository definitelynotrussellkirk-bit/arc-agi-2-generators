"""Generator for arc_additional_puzzles_21_set10_bundle:E69 — Bbox crop of target-color blob (target = (0,0)).

Rule: target color = g[0][0]. Find a blob of that color whose cells
don't include (0,0); output bbox subgrid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_matching_blob, multiple_marker_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "e2eab62ba331"
VERSION = "1.1.0"
TASK_ID = "e2eab62ba331"
SUMMARY = "Marker color at (0,0); a small blob of same color elsewhere; distractor blobs of other colors."

INVARIANTS = [
    "(0,0) holds a non-bg marker color",
    "≥1 blob of same color elsewhere (not touching (0,0))",
    "1-2 distractor blobs of different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_matching_blob", "multiple_marker_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "marker_at_origin_with_blobs",
                       "valid": "marker_at_origin_with_blobs"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    marker, c2, c3 = pal
    g[0][0] = marker
    shape = rng.choice([
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
    ])
    top = rng.randint(2, h - 4); left = rng.randint(2, w - 4)
    paint_at(g, top, left, shape, marker)
    bar = [(0, 0), (0, 1)]
    paint_at(g, 1, w - 3, bar, c2)
    g[h - 2][1] = c3; g[h - 1][2] = c3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # blobs but (0,0) is bg → no target color identifiable
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 4)
        paint_at(g, 4, 5, [(0, 0), (0, 1)], 6)
        return g
    if name == "no_matching_blob":
        # marker at (0,0) but no other blob of same color → nothing to crop
        g[0][0] = 4
        paint_at(g, 2, 2, [(0, 0), (0, 1)], 6)
        paint_at(g, 4, 5, [(0, 0), (1, 0)], 7)
        return g
    if name == "multiple_marker_blobs":
        # multiple blobs all of marker color → ambiguous which to crop
        g[0][0] = 4
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 4)
        paint_at(g, 4, 5, [(0, 0), (0, 1), (1, 0)], 4)
        return g
    return g
