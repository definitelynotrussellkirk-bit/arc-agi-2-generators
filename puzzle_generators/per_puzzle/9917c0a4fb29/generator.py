"""Generator for arc_puzzle_bank_fifth21:E34 — mirror left-side cells across full-height 9 guide.

Rule: full-height column of 9s acts as the vertical mirror axis;
left-side colored cells are mirrored to the right.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide, cells_on_right, partial_guide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9917c0a4fb29"
VERSION = "1.1.0"
TASK_ID = "9917c0a4fb29"
SUMMARY = "Place sparse cells on one side of a full-height 9 guide column to mirror across it."

INVARIANTS = [
    "background is 0",
    "one full-height guide column is color 9",
    "colored singleton cells do not sit on the guide",
    "mirror targets are in bounds and initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "cells_on_right", "partial_guide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11 odd", "valid": "5..17 odd"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_only_full_9_guide",
                       "valid": "left_only_full_9_guide"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
        target = ctx.draw_int("markers", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        target = ctx.draw_int("markers", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        target = ctx.draw_int("markers", 3, 5)
    if w % 2 == 0:
        w += 1
    rng = ctx.draw_rng("layout")
    guide = w // 2
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][guide] = 9
    positions = [(r, c) for r in range(h) for c in range(guide)]
    rng.shuffle(positions)
    placed = 0
    for r, c in positions:
        if placed >= target:
            break
        mc = 2 * guide - c
        if g[r][mc] != 0:
            continue
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    guide = w // 2
    if name == "no_guide":
        # cells but no 9-guide → no mirror axis defined
        g[1][2] = 4; g[3][3] = 6
        return g
    if name == "cells_on_right":
        # cells already on right side → mirror would clobber
        for r in range(h): g[r][guide] = 9
        g[1][1] = 4; g[2][2] = 6   # left
        g[1][7] = 3; g[2][6] = 7   # right (clobber)
        return g
    if name == "partial_guide":
        # guide has gaps → "full-height" precondition fails
        for r in range(h - 2): g[r][guide] = 9
        g[1][1] = 4; g[2][2] = 6
        return g
    return g
