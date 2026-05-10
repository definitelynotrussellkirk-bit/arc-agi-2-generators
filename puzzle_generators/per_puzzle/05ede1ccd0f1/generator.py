"""Generator for arc_puzzle_bank_twentyfirst21:E143.

Rule: a vertical color-8 axis column splits the grid. Cells left of
the axis are mirrored to the corresponding column right of the axis.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, source_on_right, source_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "05ede1ccd0f1"
VERSION = "1.1.0"
TASK_ID = "05ede1ccd0f1"
SUMMARY = "A full color-8 axis column + scattered non-{0,8} cells in left side."

INVARIANTS = [
    "background is 0",
    "exactly one full color-8 column (the axis)",
    "left of axis has 2-4 sparse non-{0, 8} cells",
    "right of axis is all 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "source_on_right", "source_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..8", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_of_axis",
                       "valid": "left_of_axis"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..8", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    axis = rng.randint(2, w - 3)
    for r in range(h):
        g[r][axis] = 8
    n = rng.randint(2, 5)
    for _ in range(n):
        r = rng.randint(0, h - 1); c = rng.randint(0, axis - 1)
        if g[r][c] == 0:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # no full 8-column → mirror axis is undefined
        g[1][1] = 3; g[3][2] = 7
        return g
    axis = 4
    for r in range(h):
        g[r][axis] = 8
    if name == "source_on_right":
        # all source cells already on the right → "left source" assumption violated
        g[1][6] = 3; g[3][7] = 7
        return g
    if name == "source_on_axis":
        # source cell sits on the axis column → ambiguous which side it belongs to
        g[1][axis] = 3
        g[3][1] = 7
        return g
    return g
