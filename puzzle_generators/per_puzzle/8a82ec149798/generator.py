"""Generator for arc_puzzle_bank_21_set9_e:medium_i13 — vertical 5-divider mirror.

Rule: a vertical color-5 divider column splits the grid. Non-{0, 5} cells
on the left are mirrored to the right.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, partial_divider, cells_on_right.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a82ec149798"
VERSION = "1.1.0"
TASK_ID = "8a82ec149798"
SUMMARY = "Full color-5 vertical divider + 2-4 non-{0, 5} cells on the left."

INVARIANTS = [
    "background is 0",
    "exactly one full color-5 column (the divider)",
    "left of divider has 2-4 sparse non-{0, 5} cells; right of divider is bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "partial_divider", "cells_on_right")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_only_5div",
                       "valid": "left_only_5div"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    div = rng.randint(2, w - 4)
    for r in range(h):
        g[r][div] = 5
    for _ in range(rng.randint(2, 4)):
        for _t in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, div - 1)
            if g[r][c] != 0: continue
            mc = 2 * div - c
            if not (0 <= mc < w): continue
            g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    div = w // 2
    if name == "no_divider":
        # no 5-column → axis undefined
        g[1][1] = 4; g[3][2] = 6
        return g
    if name == "partial_divider":
        # divider has gaps → "full color-5 column" precondition fails
        for r in range(h - 2): g[r][div] = 5
        g[1][1] = 4; g[2][2] = 6
        return g
    if name == "cells_on_right":
        # cells on right side → mirror would clobber existing right-side content
        for r in range(h): g[r][div] = 5
        g[1][1] = 4; g[2][2] = 6   # left
        g[1][7] = 3; g[2][8] = 7   # right (clobber)
        return g
    return g
