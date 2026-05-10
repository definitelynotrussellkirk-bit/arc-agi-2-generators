"""Generator for arc_additional_puzzles_21_set12_bundle:M80.

Rule: sort objects by (color asc, r1 asc, c1 asc); produce N×N matrix
where (r,c) = 8 if obj r matches obj c under any rotation, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_unique, single_object, all_identical.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "df3185f767ea"
VERSION = "1.1.0"
TASK_ID = "df3185f767ea"
SUMMARY = "3 small, well-separated, distinct-color shapes — at least 2 share rotation equivalence."

INVARIANTS = [
    "exactly 3 connected non-bg objects (4-connectivity)",
    "distinct colors, sizes ≤ 4",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_unique", "single_object", "all_identical")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread",
                       "valid": "spread"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 6, 7, 8], 3)
    L = [(0, 0), (1, 0), (1, 1)]
    Lrot = [(0, 0), (0, 1), (1, 1)]
    different = [(0, 0), (0, 1), (0, 2)]
    shapes = [L, Lrot, different]
    rng.shuffle(shapes)
    paint_at(g, 1, 1, shapes[0], pal[0])
    paint_at(g, 1, w - 4, shapes[1], pal[1])
    paint_at(g, h - 4, 3, shapes[2], pal[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "all_unique":
        # all 3 shapes pairwise rotation-inequivalent → off-diagonal matrix all 0
        s1 = [(0, 0), (0, 1), (0, 2)]  # I3
        s2 = [(0, 0), (0, 1), (1, 0), (1, 1)]  # square
        s3 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]  # L5
        paint_at(g, 1, 1, s1, 4)
        paint_at(g, 1, w - 4, s2, 6)
        paint_at(g, h - 4, 3, s3, 7)
        return g
    if name == "single_object":
        # one object → matrix is 1x1, no comparison possible
        paint_at(g, 3, 5, [(0, 0), (1, 0), (1, 1)], 4)
        return g
    if name == "all_identical":
        # all 3 shapes identical → matrix is all 8 (saturated)
        common = [(0, 0), (1, 0), (1, 1)]
        paint_at(g, 1, 1, common, 4)
        paint_at(g, 1, w - 4, common, 6)
        paint_at(g, h - 4, 3, common, 7)
        return g
    return g
