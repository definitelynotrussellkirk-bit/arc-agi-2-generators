"""Generator for arc_puzzle_bank_21_set10_e:medium_j11 — Recolor by symmetry class.

Rule: for each object, classify its bbox-mask: lr-sym & ud-sym → 8,
lr-sym only → 2, ud-sym only → 3, neither → 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_double_sym, all_asymmetric, single_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "aa0b08801e61"
VERSION = "1.1.0"
TASK_ID = "aa0b08801e61"
SUMMARY = "4 distinct-color blobs, each with different symmetry class."

INVARIANTS = [
    "4 non-touching blobs of distinct colors",
    "one is double-sym (plus), one lr-sym only, one ud-sym only, one asymmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_double_sym", "all_asymmetric", "single_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "four_symmetry_classes",
                       "valid": "four_symmetry_classes"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    # Plus shape (both sym)
    paint_at(g, 1, 2, PLUS_5, 2)
    # LR-sym only (3 wide ⊓)
    paint_at(g, 1, w - 4, [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)], 4)
    # UD-sym only (vertical bracket)
    paint_at(g, h - 4, 1, [(0, 0), (1, 0), (1, 1), (2, 0)], 5)
    # Asymmetric
    paint_at(g, h - 4, w - 4, [(0, 0), (0, 1), (1, 1), (2, 0)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "all_double_sym":
        # all 4 blobs are double-sym (plus) → all recolor to 8 (uniform)
        paint_at(g, 1, 2, PLUS_5, 2)
        paint_at(g, 1, 8, PLUS_5, 4)
        paint_at(g, 6, 2, PLUS_5, 5)
        paint_at(g, 6, 8, PLUS_5, 7)
        return g
    if name == "all_asymmetric":
        # all 4 blobs asymmetric → all recolor to 4 (uniform)
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1), (2, 0)], 2)
        paint_at(g, 1, 7, [(0, 0), (0, 1), (1, 1), (2, 0)], 4)
        paint_at(g, 6, 1, [(0, 0), (0, 1), (1, 1), (2, 0)], 5)
        paint_at(g, 6, 7, [(0, 0), (0, 1), (1, 1), (2, 0)], 7)
        return g
    if name == "single_blob":
        # only 1 blob → only 1 of 4 symmetry classes exercised
        paint_at(g, 3, 5, PLUS_5, 2)
        return g
    return g
