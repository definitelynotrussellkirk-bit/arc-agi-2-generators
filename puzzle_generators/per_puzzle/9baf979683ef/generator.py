"""Generator for arc_puzzle_bank_21_set9_s:S9_E5.

Rule: objects on the left of a vertical color-5 divider are mirrored to the
right side.

Combinatorial axes (8): grid_h, grid_w, palette_kind, left_cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_left_cells, cells_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9baf979683ef"
VERSION = "1.1.0"
TASK_ID = "9baf979683ef"
SUMMARY = "Objects on the left of a full color-5 divider are mirrored to the right side."

INVARIANTS = [
    "background is 0",
    "one full-height vertical divider column is color 5",
    "all non-divider objects begin left of the divider",
    "the mirrored right-side locations are in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_left_cells", "cells_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng odd 9..13", "valid": "7..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "left_cell_count": {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "vertical_divider_with_left_cells",
                       "valid": "vertical_divider_with_left_cells"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 9)
        count = ctx.draw_int("left_cell_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        count = ctx.draw_int("left_cell_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        count = ctx.draw_int("left_cell_count", 3, 5)
    if w % 2 == 0:
        w += 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    div = w // 2
    for r in range(h):
        g[r][div] = 5
    placed = set()
    palette = [2, 3, 4, 6, 7]
    for i in range(count):
        for _ in range(80):
            r = rng.randrange(h)
            c = rng.randrange(div)
            if (r, c) not in placed:
                g[r][c] = palette[i % len(palette)]
                placed.add((r, c))
                break
    return g


def _draw_from_degenerate(name, rng):
    h = 8; w = 11; div = w // 2
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # missing color-5 column → no axis to mirror across
        g[1][1] = 4; g[3][2] = 6; g[5][3] = 3
        return g
    if name == "no_left_cells":
        # divider present but no left-side cells → rule has nothing to mirror
        for r in range(h):
            g[r][div] = 5
        return g
    if name == "cells_both_sides":
        # cells on both sides of divider → which side is "the source"?
        for r in range(h):
            g[r][div] = 5
        g[1][1] = 4; g[3][2] = 6  # left side
        g[2][7] = 3; g[4][9] = 8  # right side
        return g
    return g
