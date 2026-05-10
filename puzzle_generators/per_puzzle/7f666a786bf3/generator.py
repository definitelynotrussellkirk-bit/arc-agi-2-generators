"""Generator for arc_puzzle_bank_21_set4_d:medium_d07.

Rule: each color's sparse cells define a bounding box; fill the box.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_cell_color, overlapping_bboxes, no_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7f666a786bf3"
VERSION = "1.1.0"
TASK_ID = "7f666a786bf3"
SUMMARY = "Sparse same-color corner cells whose per-color bounding boxes should fill."

INVARIANTS = [
    "background is 0",
    "each nonzero color appears as two to four sparse cells",
    "each color's bounding box contains at least one zero to be filled",
    "different colors' bounding boxes do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_cell_color", "overlapping_bboxes", "no_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse_corners",
                       "valid": "sparse_corners"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    boxes = [(1, 1, 3, 4), (1, w - 6, 4, w - 2), (h - 5, 3, h - 2, 7)]
    for color, (r1, c1, r2, c2) in zip(colors, boxes):
        g[r1][c1] = color
        g[r1][c2] = color
        g[r2][c1] = color
        if rng.choice([True, False]):
            g[r2][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "single_cell_color":
        # at least one color has only 1 cell → bbox is degenerate (1×1), nothing to fill
        g[2][2] = 4
        g[1][8] = 5; g[1][12] = 5; g[4][8] = 5
        g[h - 3][3] = 7; g[h - 3][6] = 7; g[h - 5][3] = 7
        return g
    if name == "overlapping_bboxes":
        # two colors' bboxes overlap → fill of overlap region is ambiguous
        g[1][1] = 4; g[1][6] = 4; g[4][1] = 4; g[4][6] = 4
        g[2][3] = 5; g[2][8] = 5; g[5][3] = 5; g[5][8] = 5
        return g
    if name == "no_colors":
        # empty grid → no boxes to define or fill
        return g
    return g
