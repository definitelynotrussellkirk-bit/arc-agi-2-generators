"""Generator for arc_puzzle_bank_twentieth21:E137.

Rule: a horizontal color-8 axis row separates the grid. Cells above
the axis are mirrored to the corresponding row below.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, source_below, source_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a279b104523"
VERSION = "1.1.0"
TASK_ID = "4a279b104523"
SUMMARY = "A full color-8 axis row + scattered non-{0,8} cells above the axis."

INVARIANTS = [
    "background is 0",
    "exactly one full color-8 row (the axis)",
    "rows above the axis have 2-4 sparse non-{0, 8} cells",
    "rows below the axis are all 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "source_below", "source_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..8", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "above_axis",
                       "valid": "above_axis"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 5, 7)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    axis = rng.randint(2, h - 3)
    for c in range(w):
        g[axis][c] = 8
    n = rng.randint(2, 5)
    for _ in range(n):
        r = rng.randint(0, axis - 1)
        c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 6
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # no full 8-row → mirror axis is undefined
        g[1][1] = 3; g[2][3] = 7
        return g
    axis = 4
    for c in range(w):
        g[axis][c] = 8
    if name == "source_below":
        # all source cells already below the axis → "above source" assumption violated
        g[5][1] = 3; g[6][2] = 7
        return g
    if name == "source_on_axis":
        # source overlaps the axis row → ambiguous which side it belongs to
        g[axis][2] = 3
        g[1][3] = 7
        return g
    return g
