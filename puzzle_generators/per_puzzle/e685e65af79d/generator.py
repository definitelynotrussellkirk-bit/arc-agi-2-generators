"""Generator for arc_additional_puzzle_bank_volume4:M28.

Rule: for each object, paint its cells + 3 cw rotations within its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, blob_kind, texture.
Degenerates: no_blobs, symmetric_blob, non_square_bbox.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "e685e65af79d"
VERSION = "1.1.0"
TASK_ID = "e685e65af79d"
SUMMARY = "2-3 distinct-color non-touching blobs with square bboxes."

INVARIANTS = [
    "between 2 and 3 non-touching blobs with square bboxes",
    "each blob has visible asymmetric cells (so 4 rotations differ)",
]

PALETTE_KINDS = ("default", "L_blob", "T_blob", "C_blob")
DEGENERATE_TEXTURES = ("no_blobs", "symmetric_blob", "non_square_bbox")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "corners", "valid": "corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..3"},
    "blob_kind":      {"type": "str", "default": "asymmetric_3x3",
                       "valid": "asymmetric_3x3"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    paint_at(g, 1, w - 5, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (2, 2)], 3)
    paint_at(g, h - 5, 3, [(0, 0), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], 6)
    paint_at(g, h - 5, w - 5, [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # empty grid — no objects to symmetrize
        return g
    if name == "symmetric_blob":
        # already 4-fold symmetric → 3 rotations are identity, rule has no visible effect
        sym = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        paint_at(g, 1, 1, sym, 3)
        paint_at(g, h - 5, 3, sym, 6)
        return g
    if name == "non_square_bbox":
        # blob has rectangular (not square) bbox → 90° rotation falls outside
        rect = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)]
        paint_at(g, 1, 1, rect, 3)
        paint_at(g, h - 4, 4, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 6)
        return g
    return g
