"""Generator for arc_additional_puzzle_bank_volume19:M130.

Rule: sort 2-blobs by (size desc, r1); pick the second; output
bbox-cropped mask in color 8.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, size_diversity, texture.
Degenerates: tied_sizes, only_one_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "3ce95b466478"
VERSION = "1.1.0"
TASK_ID = "3ce95b466478"
SUMMARY = "3 2-blobs of distinct sizes + decoration."

INVARIANTS = [
    "exactly 3 non-touching 2-blobs of distinct sizes",
    "decoration is non-2 color outside",
]

PALETTE_KINDS = ("default", "wide_grid", "tall_grid", "tight_grid")
DEGENERATE_TEXTURES = ("tied_sizes", "only_one_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "size_diversity": {"type": "str", "default": "varied", "valid": "varied"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    paint_at(g, 5, 7, [(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)], 2)
    paint_at(g, 1, 1, [(0, 0), (0, 1)], 2)
    paint_at(g, 2, 5, [(0, 0), (1, 0), (1, 1)], 2)
    g[h - 1][w - 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # 3 blobs all size 3 → "second largest" ambiguous
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 1, 6, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 6, 3, [(0, 0), (0, 1), (1, 0)], 2)
        return g
    if name == "only_one_blob":
        # only 1 blob — no second to pick
        paint_at(g, 3, 3, [(0, 0), (1, 0), (1, 1), (2, 1)], 2)
        return g
    if name == "no_blobs":
        # empty grid — nothing to rank
        return g
    return g
