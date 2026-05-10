"""Generator for arc_additional_puzzles_21_set10_bundle:E70 — Mirror left side over full-height 5-divider to right.

Rule: find full-height col of 5s; for each non-bg/non-5 cell on the
left, mirror to right side at column 2*gc - c.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, cells_on_right, partial_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cddbee92b2f3"
VERSION = "1.1.0"
TASK_ID = "cddbee92b2f3"
SUMMARY = "Full-height 5-divider in middle; left side has scattered single colors."

INVARIANTS = [
    "exactly 1 full-height col of 5s",
    "left side has 2-3 isolated non-5 cells",
    "right side is all 0 (so mirror is visible)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "cells_on_right", "partial_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_side_only_with_full_5div",
                       "valid": "left_side_only_with_full_5div"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    gc = w // 2
    for r in range(h):
        g[r][gc] = 5
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    n = rng.randint(2, 3)
    for _ in range(n):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, gc - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    gc = w // 2
    if name == "no_divider":
        # no 5-divider → axis undefined, no mirror possible
        g[1][1] = 4; g[3][2] = 6
        return g
    if name == "cells_on_right":
        # cells on right side → mirror would clobber existing right-side content
        for r in range(h): g[r][gc] = 5
        g[1][1] = 4   # left
        g[2][7] = 6   # right (clobber)
        g[3][8] = 3   # right (clobber)
        return g
    if name == "partial_divider":
        # divider has gaps → "full-height col of 5s" precondition fails
        for r in range(h - 2): g[r][gc] = 5
        g[1][1] = 4; g[2][2] = 6
        return g
    return g
