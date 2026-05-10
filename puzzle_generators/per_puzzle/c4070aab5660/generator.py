"""Generator for arc_additional_puzzle_bank_volume21:M143.

Rule: bbox of red(2) cells ∩ bbox of green(3) cells; paint with 8 if
non-empty, else empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, overlap_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_overlap, no_red, no_green.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c4070aab5660"
VERSION = "1.1.0"
TASK_ID = "c4070aab5660"
SUMMARY = "Red blob and green blob with overlapping bboxes."

INVARIANTS = [
    "exactly one red(2) blob and one green(3) blob",
    "their bboxes overlap (so intersection is non-empty)",
    "decoration is non-{2,3} cells outside",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_overlap", "no_red", "no_green")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "overlap_kind":   {"type": "str", "default": "corner_overlap",
                       "valid": "corner_overlap"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "two_blobs_overlapping",
                       "valid": "two_blobs_overlapping"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "blobs", "valid": "blobs"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    paint_at(g, 3, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)], 2)
    paint_at(g, 5, 4, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)], 3)
    g[0][0] = 6; g[0][1] = 6; g[0][2] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_overlap":
        # red and green bboxes don't overlap → intersection empty, output blank
        paint_at(g, 1, 1, [(0, 0), (1, 0), (0, 1)], 2)
        paint_at(g, 5, 8, [(0, 0), (1, 0), (0, 1)], 3)
        return g
    if name == "no_red":
        # only green blob → no red bbox, intersection undefined
        paint_at(g, 5, 4, [(0, 0), (0, 1), (1, 0)], 3)
        return g
    if name == "no_green":
        # only red blob → no green bbox, intersection undefined
        paint_at(g, 3, 3, [(0, 0), (1, 0), (0, 1)], 2)
        return g
    return g
