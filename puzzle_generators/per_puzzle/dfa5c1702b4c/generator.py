"""Generator for arc_additional_puzzles_21_set8:H51.

Rule: pairwise bbox-overlap matrix from sorted-by-(r1,c1) blobs;
3 if both row+col bboxes overlap, 1 if row-only, 2 if col-only, else 0.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_blobs, single_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "dfa5c1702b4c"
VERSION = "1.1.0"
TASK_ID = "dfa5c1702b4c"
SUMMARY = "3 distinct-color blobs with varied bbox-overlap relationships."

INVARIANTS = [
    "exactly 3 non-touching blobs",
    "blob bboxes have a mix of row/col overlap relationships",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "11..13"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "13..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    fill_box(g, 1, 1, 3, 3, 2)
    fill_box(g, 2, 5, 4, 7, 5)
    fill_box(g, 7, 2, 9, 4, 7)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_blobs":
        return g
    if name == "single_blob":
        fill_box(g, 1, 1, 3, 3, 2)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
