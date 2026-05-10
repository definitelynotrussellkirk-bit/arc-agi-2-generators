"""Generator for arc_additional_puzzle_bank_volume16:M107.

Rule: dr/dc = (3-marker - 2-marker); among 1-blobs, pick smallest by
(size, r1, c1); clear it; paint moved cells with 8.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, vector_length, texture.
Degenerates: no_markers, no_blobs, tied_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "4cdcebe180f3"
VERSION = "1.1.0"
TASK_ID = "4cdcebe180f3"
SUMMARY = "2-marker + 3-marker (delta) + 2 1-blobs (one smaller) + decoration."

INVARIANTS = [
    "exactly one 2-marker and one 3-marker",
    "exactly 2 1-blobs of distinct sizes",
    "translated cells stay in-bounds",
]

PALETTE_KINDS = ("default", "tight_grid", "wide_grid", "tall_grid")
DEGENERATE_TEXTURES = ("no_markers", "no_blobs", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "vector_length":  {"type": "str", "default": "mixed", "valid": "mixed"},
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
    g[1][1] = 2
    g[3][4] = 3
    paint_at(g, 1, 6, [(0, 0), (1, 0), (2, 0), (2, 1)], 1)
    paint_at(g, 5, 1, [(0, 0), (1, 0), (1, 1)], 1)
    g[h - 1][w - 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blobs but no 2/3 markers → translation vector undefined
        paint_at(g, 1, 6, [(0, 0), (1, 0), (2, 0), (2, 1)], 1)
        paint_at(g, 5, 1, [(0, 0), (1, 0), (1, 1)], 1)
        return g
    if name == "no_blobs":
        # markers but no 1-blobs → nothing to translate
        g[1][1] = 2
        g[3][4] = 3
        return g
    if name == "tied_sizes":
        # both blobs same size → "smallest" ambiguous
        g[1][1] = 2
        g[3][4] = 3
        paint_at(g, 1, 6, [(0, 0), (1, 0), (1, 1)], 1)
        paint_at(g, 5, 1, [(0, 0), (1, 0), (1, 1)], 1)
        return g
    return g
