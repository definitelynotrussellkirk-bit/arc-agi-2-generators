"""Generator for arc_puzzle_bank_21_set14_bundle:easy_n06.

Same-color plus signs are present. The rule fills their four diagonal corners
to create solid 3x3 squares.

Combinatorial axes (8): grid_h, grid_w, palette_kind, plus_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, plus_at_edge, already_solid_squares.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d9d4f0ebb48b"
VERSION = "1.1.0"
TASK_ID = "d9d4f0ebb48b"
SUMMARY = "Separated interior plus signs ready to grow into 3x3 squares."

INVARIANTS = [
    "background is 0",
    "each object is a five-cell plus shape",
    "plus centers are interior cells",
    "3x3 neighborhoods for pluses do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "plus_at_edge", "already_solid_squares")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "plus_count":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_pluses",
                       "valid": "spaced_pluses"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _square_cells(r, c):
    return {(rr, cc) for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        plus_count = ctx.draw_int("plus_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        plus_count = ctx.draw_int("plus_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        plus_count = ctx.draw_int("plus_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=plus_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            r = rng.randint(1, h - 2)
            c = rng.randint(1, w - 2)
            square = _square_cells(r, c)
            if not (square & occupied):
                for rr, cc in [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                    g[rr][cc] = color
                occupied |= square
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # blank → no objects to grow, output identical to input
        return g
    if name == "plus_at_edge":
        # plus centered on border row → diagonals fall off-grid
        g[0][3] = 4; g[1][2] = 4; g[1][3] = 4; g[1][4] = 4
        # missing top arm cell because r=0
        return g
    if name == "already_solid_squares":
        # solid 3x3 squares → rule's "fill diagonals" is no-op
        for r in range(1, 4):
            for c in range(1, 4): g[r][c] = 4
        for r in range(5, 8):
            for c in range(5, 8): g[r][c] = 6
        return g
    return g
