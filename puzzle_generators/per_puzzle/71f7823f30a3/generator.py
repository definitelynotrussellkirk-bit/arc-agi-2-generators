"""Generator for arc_puzzle_bank_twentythird21:E161.

Rule: a full color-9 column is the axis. Cells left of the axis
(non-{0, 9}) are mirrored to the corresponding column right of the
axis.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, source_on_right, source_on_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "71f7823f30a3"
VERSION = "1.1.0"
TASK_ID = "71f7823f30a3"
SUMMARY = "A full color-9 axis column + scattered non-{0, 9} cells in left side."

INVARIANTS = [
    "background is 0",
    "exactly one full color-9 column (the axis)",
    "left of axis has 2-4 sparse non-{0, 9} cells",
    "right of axis is all 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "source_on_right", "source_on_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    axis = rng.randint(2, w - 4)
    for r in range(h):
        g[r][axis] = 9
    n = rng.randint(2, 5)
    for _ in range(n):
        r = rng.randint(0, h - 1); c = rng.randint(0, axis - 1)
        if g[r][c] == 0:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 8
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # no full 9-column → mirror axis is undefined
        g[1][1] = 3; g[3][2] = 7
        return g
    axis = 4
    for r in range(h):
        g[r][axis] = 9
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
