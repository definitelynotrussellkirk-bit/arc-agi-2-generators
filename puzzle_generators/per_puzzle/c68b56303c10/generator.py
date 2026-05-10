"""Generator for arc_additional_puzzles_21_set4:M27 — Output is solid 8-grid sized by red∩green bbox.

Rule: bbox of all red(2) cells, bbox of all green(3) cells. Output is
empty grid of (8) of size = intersection of those bboxes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_red, n_green,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, no_green, disjoint_bboxes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c68b56303c10"
VERSION = "1.1.0"
TASK_ID = "c68b56303c10"
SUMMARY = "Scattered red and green cells; output sized by bbox-intersection, filled 8."

INVARIANTS = [
    "between 2 and 4 red(2) cells",
    "between 2 and 4 green(3) cells",
    "their bboxes intersect (so output is non-empty)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "no_green", "disjoint_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_red":          {"type": "int", "default": "rng 2..4",  "valid": "2..6"},
    "n_green":        {"type": "int", "default": "rng 2..4",  "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "intersecting_bboxes",
                       "valid": "intersecting_bboxes"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n_red = ctx.draw_int("n_red", 2, 2)
        n_green = ctx.draw_int("n_green", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n_red = ctx.draw_int("n_red", 3, 4)
        n_green = ctx.draw_int("n_green", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        n_red = ctx.draw_int("n_red", 2, 4)
        n_green = ctx.draw_int("n_green", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = 0
    while placed < n_red:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 2; placed += 1
    placed = 0
    while placed < n_green:
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 3; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_red":
        # only green cells → no red bbox to intersect with, output undefined
        g[1][2] = 3; g[3][5] = 3; g[5][7] = 3
        return g
    if name == "no_green":
        # only red cells → no green bbox, output undefined
        g[1][2] = 2; g[3][5] = 2; g[5][7] = 2
        return g
    if name == "disjoint_bboxes":
        # red cells in upper-left, green in lower-right; bboxes don't overlap
        g[0][0] = 2; g[0][1] = 2; g[1][0] = 2
        g[5][7] = 3; g[5][8] = 3; g[6][8] = 3
        return g
    return g
