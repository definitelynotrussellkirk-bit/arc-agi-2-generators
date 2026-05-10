"""Generator for arc_puzzle_bank_21_set16_bundle:easy_p04.

Solid monochrome 3x3 squares are reduced to their four corners.

Combinatorial axes (8): grid_h, grid_w, palette_kind, square_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_squares, hollow_squares, wrong_size_squares.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "a06827026857"
VERSION = "1.1.0"
TASK_ID = "a06827026857"
SUMMARY = "Separated solid 3x3 monochrome squares."

INVARIANTS = [
    "background is 0",
    "each object is a solid 3x3 square",
    "3x3 squares are separated by at least one row/column of background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_squares", "hollow_squares", "wrong_size_squares")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..15"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "square_count":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "separated_3x3_squares",
                       "valid": "separated_3x3_squares"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _zone(r, c):
    return {(rr, cc) for rr in range(r - 1, r + 4) for cc in range(c - 1, c + 4)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        square_count = ctx.draw_int("square_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        square_count = ctx.draw_int("square_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        square_count = ctx.draw_int("square_count", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=square_count, exclude={0})
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            r = rng.randint(0, h - 3)
            c = rng.randint(0, w - 3)
            zone = _zone(r, c)
            if not (zone & occupied):
                fill_box(g, r, c, r + 2, c + 2, color)
                occupied |= zone
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_squares":
        # blank → no 3x3 squares to reduce
        return g
    if name == "hollow_squares":
        # 3x3 frames (only outer ring filled) → already match the rule's output (no-op)
        for r, c in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]:
            g[r][c] = 4
        return g
    if name == "wrong_size_squares":
        # 2x2 squares → "solid 3x3" precondition fails
        for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            g[r][c] = 4
        for r, c in [(5, 5), (5, 6), (6, 5), (6, 6)]:
            g[r][c] = 6
        return g
    return g
