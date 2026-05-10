"""Generator for arc_additional_puzzle_bank_volume19:M128.

Rule: a full gray divider column reflects blue cells to cyan on an
otherwise blank output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blue_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_blue, blue_on_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4f6f232c17bc"
VERSION = "1.1.0"
TASK_ID = "4f6f232c17bc"
SUMMARY = "A full gray divider column reflects blue cells to cyan on an otherwise blank output."
INVARIANTS = [
    "exactly one full color-5 divider column",
    "all color-1 cells lie on one side of the divider",
    "reflected color-1 positions remain inside the grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_blue", "blue_on_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blue_size":      {"type": "int", "default": "rng 4..8", "valid": "1..16"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "left_blue_full_divider",
                       "valid": "left_blue_full_divider"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        half_w = ctx.draw_int("half_w", 4, 4)
        size = ctx.draw_int("blue_size", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        half_w = ctx.draw_int("half_w", 5, 6)
        size = ctx.draw_int("blue_size", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        half_w = ctx.draw_int("half_w", 4, 6)
        size = ctx.draw_int("blue_size", 4, 8)
    rng = ctx.draw_rng("layout")

    w = half_w * 2 + 1
    div = half_w
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][div] = 5

    cells = grow_blob(rng, h, half_w - 1, set(), size)
    if cells is None:
        cells = {(1, 1), (1, 2), (2, 1), (3, 1)}
    for r, c in cells:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # blue cells without 5-divider → no reflection axis
        g[2][1] = 1; g[3][2] = 1; g[4][1] = 1
        return g
    if name == "no_blue":
        # divider but no blue cells → nothing to reflect
        for r in range(h): g[r][4] = 5
        return g
    if name == "blue_on_both_sides":
        # blue on both sides of divider → reflection collides with existing cells
        for r in range(h): g[r][4] = 5
        g[2][1] = 1; g[3][2] = 1
        g[2][7] = 1; g[3][6] = 1
        return g
    return g
