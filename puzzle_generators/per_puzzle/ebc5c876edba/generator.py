"""Generator for v3_rich_schema:easy_06_mirror_object_across_bar — mirror across vertical 5-bar.

Rule: a vertical color-5 bar splits the grid. Color-2 cells on one side are
mirrored across the bar in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_bar, no_cells, cells_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ebc5c876edba"
VERSION = "1.1.0"
TASK_ID = "ebc5c876edba"

SUMMARY = "Vertical color-5 bar + color-2 motif on one side."

INVARIANTS = [
    "background is 0",
    "exactly one full color-5 column (the bar)",
    "left of bar has 2-4 color-2 cells; right of bar is bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bar", "no_cells", "cells_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "vertical_bar_with_left_motif",
                       "valid": "vertical_bar_with_left_motif"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    bar_col = rng.randint(2, w - 4)
    for r in range(h):
        g[r][bar_col] = 5
    n = rng.randint(2, 4)
    for _ in range(n):
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, bar_col - 1)
            if g[r][c] != 0: continue
            mc = 2 * bar_col - c
            if not (0 <= mc < w): continue
            g[r][c] = 2
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_bar":
        # missing color-5 column → rule has no axis to mirror across
        g[1][1] = 2; g[3][2] = 2; g[5][3] = 2
        return g
    if name == "no_cells":
        # bar present but no color-2 cells → rule has nothing to mirror
        bar_col = 4
        for r in range(h):
            g[r][bar_col] = 5
        return g
    if name == "cells_both_sides":
        # color-2 cells on both sides of bar → which side is "the source"?
        bar_col = 4
        for r in range(h):
            g[r][bar_col] = 5
        g[1][1] = 2; g[3][2] = 2  # left side
        g[2][6] = 2; g[4][7] = 2  # right side
        return g
    return g
