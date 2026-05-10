"""Generator for arc_puzzle_bank_21_set24_s:S24_E6.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_distractors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_distractors, tied_depth, single_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "144e23365d4b"
VERSION = "1.1.0"
TASK_ID = "144e23365d4b"
SUMMARY = "Only the component with the greatest onion depth is kept and recolored."

INVARIANTS = [
    "background is 0",
    "one rectangle has strictly greater max onion depth than the distractors",
    "the selected component is recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_distractors", "tied_depth", "single_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "9..20"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distractors":  {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "big_rect_plus_distractors",
                       "valid": "big_rect_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_rect(grid, r0, c0, rh, rw, color):
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            grid[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7], 3)
    big_h = rng.randint(6, min(8, h - 2))
    big_w = rng.randint(6, min(8, w - 7))
    big_r = rng.randint(0, h - big_h)
    big_c = rng.randint(0, max(0, w - big_w - 7))
    _paint_rect(grid, big_r, big_c, big_h, big_w, colors[0])
    right_start = big_c + big_w + 2
    for i in range(2):
        rh = rng.randint(3, 4)
        rw = rng.randint(3, 4)
        r0 = rng.randint(0, h - rh)
        c0 = min(w - rw, right_start + i * 4)
        _paint_rect(grid, r0, c0, rh, rw, colors[i + 1])
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 13, 16
    g = full_grid(h, w, 0)
    if name == "no_distractors":
        # only the big rectangle → trivially highest depth, no contrast
        _paint_rect(g, 2, 2, 7, 7, 3)
        return g
    if name == "tied_depth":
        # rectangles share max onion depth → ambiguous winner
        _paint_rect(g, 1, 1, 5, 5, 3)
        _paint_rect(g, 7, 9, 5, 5, 4)
        return g
    if name == "single_rect":
        # a single small rect has max depth 1 → no real onion depth signal
        _paint_rect(g, 5, 5, 3, 3, 3)
        return g
    return g
