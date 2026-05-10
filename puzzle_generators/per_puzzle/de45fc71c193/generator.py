"""Generator for arc_puzzle_bank_21_set5_e:medium_e07 — overlap of color bboxes.

Rule: each color has a bbox (computed from its cells). Output: cells in
the rectangular intersection of the two bboxes painted in 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_colors, single_color, disjoint_bboxes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "de45fc71c193"
VERSION = "1.1.0"
TASK_ID = "de45fc71c193"
SUMMARY = "Two colors each with 4 corner cells; bboxes overlap in a non-empty rect."

INVARIANTS = [
    "background is 0",
    "exactly 2 distinct non-zero colors",
    "each color has ≥2 cells defining a bbox",
    "the two bboxes overlap (intersection rect is non-empty)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_colors", "single_color", "disjoint_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_overlapping_bboxes",
                       "valid": "two_overlapping_bboxes"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7], 2)
    a1r = 1; a2r = h - 3
    a1c = 1; a2c = w // 2 + 1
    g[a1r][a1c] = palette[0]
    g[a2r][a2c] = palette[0]
    b1r = 2; b2r = h - 2
    b1c = w // 2 - 1; b2c = w - 2
    if g[b1r][b1c] == 0:
        g[b1r][b1c] = palette[1]
    if g[b2r][b2c] == 0:
        g[b2r][b2c] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_colors":
        # blank → no bboxes to intersect
        return g
    if name == "single_color":
        # only one color → no second bbox to intersect with
        g[1][1] = 4
        g[5][7] = 4
        return g
    if name == "disjoint_bboxes":
        # two colors but their bboxes don't overlap → empty intersection
        g[1][1] = 4; g[2][3] = 4    # bbox top-left quadrant
        g[5][6] = 6; g[6][8] = 6    # bbox bottom-right, no overlap
        return g
    return g
