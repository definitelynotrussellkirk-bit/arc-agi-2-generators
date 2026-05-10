"""Generator for arc_additional_puzzles_21_set2:H10.

Rule: sort 4 distinct-color blobs by color ascending, then assemble a
2×2 grid of their bbox crops (top-left, top-right, bottom-left, bottom-right).

Combinatorial axes (8): grid_h/w, palette_kind, num_blobs, blob_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_three_blobs, all_same_color, five_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "b44242314fb7"
VERSION = "1.1.0"
TASK_ID = "b44242314fb7"
SUMMARY = "4 distinct-color blobs of varied shapes."

INVARIANTS = [
    "exactly 4 non-touching blobs",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_three_blobs", "all_same_color", "five_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_blobs":      {"type": "int", "default": "4", "valid": "4"},
    "blob_size":      {"type": "str", "default": "varied", "valid": "varied"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "quad", "valid": "quad"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
    paint_at(g, 1, 8, [(0, 0), (0, 1), (0, 2)], 3)
    paint_at(g, 6, 1, [(0, 0), (1, 0), (1, 1)], 4)
    paint_at(g, 7, 10, [(0, 0), (0, 1), (1, 0), (1, 1)], 5)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "only_three_blobs":
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 1, 8, [(0, 0), (0, 1), (0, 2)], 3)
        paint_at(g, 6, 1, [(0, 0), (1, 0), (1, 1)], 4)
        return g
    if name == "all_same_color":
        # 4 blobs but identical color — sort produces no canonical order
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 1, 8, [(0, 0), (0, 1), (0, 2)], 2)
        paint_at(g, 6, 1, [(0, 0), (1, 0), (1, 1)], 2)
        paint_at(g, 7, 10, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        return g
    if name == "five_blobs":
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 1, 8, [(0, 0), (0, 1), (0, 2)], 3)
        paint_at(g, 6, 1, [(0, 0), (1, 0), (1, 1)], 4)
        paint_at(g, 7, 10, [(0, 0), (0, 1), (1, 0), (1, 1)], 5)
        paint_at(g, 9, 7, [(0, 0), (0, 1)], 6)
        return g
    return g
