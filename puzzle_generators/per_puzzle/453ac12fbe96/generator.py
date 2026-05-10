"""Generator for arc_puzzle_bank_21_set12_bundle:hard_l18.

Rule: normalize each object's cells; output union bbox. Cells in 2
shapes → 2; in 3 shapes → 8; else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: shapes_disjoint, single_shape, no_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "453ac12fbe96"
VERSION = "1.1.0"
TASK_ID = "453ac12fbe96"
SUMMARY = "3 distinct-color shapes that overlap (relative to bbox top-left) on multiple cells."

INVARIANTS = [
    "exactly 3 non-touching distinct-color blobs",
    "their normalized cell sets share at least one cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("shapes_disjoint", "single_shape", "no_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "tri_horizontal",
                       "valid": "tri_horizontal"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 14, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 14, 16)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    s1 = [(0, 0), (1, 0), (2, 0), (2, 1)]
    s2 = [(0, 0), (0, 1), (0, 2), (1, 1)]
    s3 = [(0, 0), (0, 1), (1, 1), (1, 2)]
    paint_at(g, 1, 1, s1, palette[0])
    paint_at(g, 1, 6, s2, palette[1])
    paint_at(g, 1, 11, s3, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 15
    g = full_grid(h, w, 0)
    if name == "shapes_disjoint":
        # normalized shapes share NO cells → output is all 0 (empty union counts)
        s1 = [(0, 0), (1, 0)]
        s2 = [(0, 1), (1, 1)]
        s3 = [(2, 0), (2, 1)]
        paint_at(g, 1, 1, s1, 4)
        paint_at(g, 1, 6, s2, 6)
        paint_at(g, 1, 11, s3, 7)
        return g
    if name == "single_shape":
        # one shape only → counts collapse to count=1, output is all 0
        paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1)], 4)
        return g
    if name == "no_shapes":
        # empty grid → no cells to count
        return g
    return g
