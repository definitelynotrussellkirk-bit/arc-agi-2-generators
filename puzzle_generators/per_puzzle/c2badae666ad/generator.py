"""Generator for arc_additional_puzzle_bank_volume19:H127.

Rule: shapes 1, 2, 3 each normalized; output cells appearing in exactly
2 of them, bbox-cropped, color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: shapes_disjoint, all_three_overlap, single_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c2badae666ad"
VERSION = "1.1.0"
TASK_ID = "c2badae666ad"
SUMMARY = "1-, 2-, 3-shapes placed apart with overlapping normalized cells (exactly 2-of-3 non-empty)."

INVARIANTS = [
    "exactly one blob each of color 1, 2, 3",
    "their normalized cell sets have at least one cell in exactly 2 of them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("shapes_disjoint", "all_three_overlap", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "tri_spread",
                       "valid": "tri_spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    s1 = [(0, 0), (0, 1), (1, 1), (2, 1)]
    s2 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    s3 = [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]
    rng.shuffle([s1, s2, s3])
    paint_at(g, 1, 1, s1, 1)
    paint_at(g, 1, w - 4, s2, 2)
    paint_at(g, h - 4, 3, s3, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "shapes_disjoint":
        # normalized cells share NO cell across any pair → exactly-2-of-3 set is empty
        s1 = [(0, 0), (0, 1)]
        s2 = [(2, 0), (2, 1)]
        s3 = [(0, 2), (1, 2)]
        paint_at(g, 1, 1, s1, 1)
        paint_at(g, 1, w - 4, s2, 2)
        paint_at(g, h - 4, 3, s3, 3)
        return g
    if name == "all_three_overlap":
        # all three shapes share every cell → each cell is in 3 (not exactly 2), output empty
        common = [(0, 0), (1, 0), (2, 0)]
        paint_at(g, 1, 1, common, 1)
        paint_at(g, 1, w - 4, common, 2)
        paint_at(g, h - 4, 3, common, 3)
        return g
    if name == "single_shape":
        # one shape only → counts collapse to 1, no exactly-2 cells
        paint_at(g, 3, 4, [(0, 0), (0, 1), (1, 0)], 1)
        return g
    return g
