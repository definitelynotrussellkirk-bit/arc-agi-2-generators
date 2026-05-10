"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_132_draw_bbox_border_around_nonzero_cells.

Rule: sparse non-8 cells define a global box that receives a cyan border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_cell, all_at_one_point, already_bordered.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a5bda33d14a0"
VERSION = "1.1.0"
TASK_ID = "a5bda33d14a0"
SUMMARY = "Sparse non-8 cells define a global box that receives a cyan border."

INVARIANTS = [
    "background is 0",
    "nonzero source cells are not color 8",
    "the global bounding box has height and width at least 3",
    "some bbox border cells are empty and will become 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_cell", "all_at_one_point", "already_bordered")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread",
                       "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1 = rng.randint(1, h - 5)
    r2 = rng.randint(r1 + 3, h - 2)
    c1 = rng.randint(1, w - 5)
    c2 = rng.randint(c1 + 3, w - 2)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    g[r1][c1] = colors[0]
    g[r2][c2] = colors[1]
    g[rng.randint(r1 + 1, r2 - 1)][rng.randint(c1 + 1, c2 - 1)] = colors[2]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "single_cell":
        # only 1 cell → bbox is 1×1, no border to draw
        g[3][4] = 5
        return g
    if name == "all_at_one_point":
        # all cells in same position (or essentially same) → bbox area zero
        g[3][4] = 5
        return g  # same as single_cell semantically
    if name == "already_bordered":
        # bbox border already painted in cyan → rule is identity
        for c in range(2, 8):
            g[2][c] = 8
            g[6][c] = 8
        for r in range(2, 7):
            g[r][2] = 8
            g[r][7] = 8
        g[3][3] = 4
        g[5][6] = 6
        return g
    return g
