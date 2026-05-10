"""Generator for arc_puzzle_bank_21_set14_bundle:easy_n04.

Three same-color corners of an axis-aligned rectangle are present. The solver
adds the missing fourth corner.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, rect_count, texture.
Degenerates: no_corners, two_corners, all_four_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d89b3f447c00"
VERSION = "1.1.0"
TASK_ID = "d89b3f447c00"
SUMMARY = "Separated three-corner rectangle clues with distinct colors."

INVARIANTS = [
    "background is 0",
    "each color appears at exactly three corners of one rectangle",
    "the fourth corner is zero",
    "different colored rectangle clues do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "two_corners", "all_four_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_count":     {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "= rect_count", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "scattered_3_corners",
                       "valid": "scattered_3_corners"},
    "n_distinct_colors": {"type": "int", "default": "= rect_count", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_area(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        rect_count = ctx.draw_int("rect_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        rect_count = ctx.draw_int("rect_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        rect_count = ctx.draw_int("rect_count", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=rect_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            r1 = rng.randint(0, h - 4)
            r2 = rng.randint(r1 + 3, h - 1)
            c1 = rng.randint(0, w - 4)
            c2 = rng.randint(c1 + 3, w - 1)
            corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
            missing = rng.randrange(4)
            cells = [p for i, p in enumerate(corners) if i != missing]
            if _clear_area(g, corners):
                for r, c in cells:
                    g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # Empty grid — rule has no rectangles to complete.
        return g
    if name == "two_corners":
        # Color appears only twice — rule's "exactly three corners"
        # filter excludes; the missing corner can't be uniquely
        # determined from 2 cells.
        g[2][2] = 4; g[5][7] = 4
        return g
    if name == "all_four_corners":
        # All four corners already present — rule's "missing corner"
        # is empty; rule's effect is invisible.
        g[2][2] = 4; g[2][7] = 4
        g[5][2] = 4; g[5][7] = 4
        return g
    return g
