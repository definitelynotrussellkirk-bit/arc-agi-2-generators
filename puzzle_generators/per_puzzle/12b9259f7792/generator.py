"""Generator for arc_additional_puzzle_bank_volume5:M31 — Recolor 5-blobs by nearest 1..4 marker.

Rule: for each 5-blob, find nearest cell with value ∈ {1,2,3,4} (Manhattan
to closest blob cell); recolor blob to that marker's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_blobs, blob_equidistant_to_two_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "12b9259f7792"
VERSION = "1.1.0"
TASK_ID = "12b9259f7792"
SUMMARY = "Corner markers (1, 2, 3, 4) + several 5-blobs each near one marker."

INVARIANTS = [
    "between 2 and 4 corner markers, each in {1,2,3,4}",
    "between 2 and 3 5-blobs, each closest to a different marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_blobs", "blob_equidistant_to_two_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "corner_markers",
                       "valid": "corner_markers"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    g[0][0] = 1
    g[0][w - 1] = 2
    g[h - 1][w - 1] = 3
    paint_at(g, 2, 1, [(0, 0), (1, 0), (1, 1)], 5)
    paint_at(g, 2, w - 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 5)
    paint_at(g, h - 3, w // 2 + 1, [(0, 0), (0, 1), (0, 2), (1, 1)], 5)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blobs without any 1..4 markers → nothing to recolor by
        paint_at(g, 2, 1, [(0, 0), (1, 0), (1, 1)], 5)
        paint_at(g, h - 3, w // 2, [(0, 0), (0, 1), (1, 0)], 5)
        return g
    if name == "no_blobs":
        # markers but no 5-blobs → rule has no targets to recolor
        g[0][0] = 1
        g[0][w - 1] = 2
        g[h - 1][w - 1] = 3
        return g
    if name == "blob_equidistant_to_two_markers":
        # blob exactly between two markers → tie-breaking is undefined
        g[0][0] = 1
        g[0][w - 1] = 2
        paint_at(g, 0, w // 2, [(0, 0), (1, 0)], 5)
        return g
    return g
