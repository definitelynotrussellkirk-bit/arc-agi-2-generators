"""Generator for arc_puzzle_bank_seventeenth21:E118 — mirror cells across full-height divider.

Rule: a full-height divider bar mirrors colored cells across its column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, partial_divider, cells_on_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4e16917b1bde"
VERSION = "1.1.0"
TASK_ID = "4e16917b1bde"
SUMMARY = "A full-height divider bar mirrors colored cells across its column."

INVARIANTS = [
    "background is 0",
    "one full-height divider column is present",
    "source cells are on one side of the divider",
    "reflected cells are in bounds and initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "partial_divider", "cells_on_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..19"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cells":          {"type": "int", "default": "rng 3..6", "valid": "1..18"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "left_only_with_full_divider",
                       "valid": "left_only_with_full_divider"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("cells", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("cells", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("cells", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    divider = rng.randint(3, w - 4)
    divider_color = rng.choice([5, 8, 9])
    for r in range(h):
        g[r][divider] = divider_color
    max_offset = min(divider, w - 1 - divider)
    candidates = [(r, divider - off) for r in range(h) for off in range(1, max_offset + 1)]
    rng.shuffle(candidates)
    source_colors = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != divider_color]
    for r, c in candidates[:target]:
        g[r][c] = rng.choice(source_colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 11
    g = full_grid(h, w, 0)
    div = w // 2
    if name == "no_divider":
        # cells but no divider → mirror axis undefined
        g[1][2] = 4; g[3][3] = 6
        return g
    if name == "partial_divider":
        # divider has gaps → "full-height" precondition fails
        for r in range(h - 2): g[r][div] = 5
        g[1][2] = 4; g[2][3] = 6
        return g
    if name == "cells_on_both_sides":
        # cells on both sides of divider → mirror would clobber existing right-side cells
        for r in range(h): g[r][div] = 5
        g[1][2] = 4; g[2][3] = 6   # left
        g[1][div + 2] = 3; g[2][div + 3] = 7   # right (clobber targets)
        return g
    return g
