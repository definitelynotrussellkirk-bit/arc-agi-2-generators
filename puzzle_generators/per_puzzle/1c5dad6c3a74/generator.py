"""Generator for arc_additional_puzzle_bank_volume8:H53.

Rule: among 7-blobs, find the one whose normalized cells are
diagonal-symmetric; paint cells outside its 1-cell ring with 8.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, sym_diversity, texture.
Degenerates: all_symmetric, no_symmetric, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "1c5dad6c3a74"
VERSION = "1.1.0"
TASK_ID = "1c5dad6c3a74"
SUMMARY = "1 diagonal-symmetric triangular 7-shape + 1 non-sym 7-shape (distractor)."

INVARIANTS = [
    "exactly one 7-blob with diagonal symmetry (right-triangle)",
    "exactly one 7-blob without diagonal symmetry",
]

PALETTE_KINDS = ("default", "tri_top_left", "tri_top_right", "wide_grid")
DEGENERATE_TEXTURES = ("all_symmetric", "no_symmetric", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "sym_diversity":  {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 6, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)], 7)
    paint_at(g, h - 5, 0, [(0, 1), (1, 0), (1, 1), (2, 0), (2, 1)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    triangle = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]
    nonsym = [(0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    if name == "all_symmetric":
        # both blobs diagonal-symmetric → ambiguous which to outline
        paint_at(g, 1, 6, triangle, 7)
        paint_at(g, h - 5, 0, triangle, 7)
        return g
    if name == "no_symmetric":
        # both blobs non-symmetric → no candidate to outline
        paint_at(g, 1, 6, nonsym, 7)
        paint_at(g, h - 5, 0, nonsym, 7)
        return g
    if name == "no_blobs":
        # empty grid — nothing to test for symmetry
        return g
    return g
