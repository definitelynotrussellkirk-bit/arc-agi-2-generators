"""Generator for arc_puzzle_bank_thirteenth_21_bundle:easy_91_complete_missing_rectangle_corner.

Rule: each color marks three corners of a rectangle; output completes
the missing fourth corner in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, rectangles, texture.
Degenerates: no_corners, two_corners, all_four_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d877a4c52fd"
VERSION = "1.1.0"
TASK_ID = "0d877a4c52fd"

SUMMARY = "Three same-color rectangle corners imply the missing fourth corner."

INVARIANTS = [
    "background is 0",
    "each color marks exactly three corners of one axis-aligned rectangle",
    "rectangle side lengths are at least 2",
    "corner sets are separated from each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "two_corners", "all_four_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "= rectangles", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_3_corners",
                       "valid": "scattered_3_corners"},
    "n_distinct_colors": {"type": "int", "default": "= rectangles", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w):
            return False
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("rectangles", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 14, 18)
        target = ctx.draw_int("rectangles", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
        target = ctx.draw_int("rectangles", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(9, target))
    placed = 0
    for _ in range(180):
        if placed >= target:
            break
        r0 = rng.randint(0, h - 3)
        r1 = rng.randint(r0 + 2, h - 1)
        c0 = rng.randint(0, w - 3)
        c1 = rng.randint(c0 + 2, w - 1)
        corners = [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]
        missing = rng.randrange(4)
        cells = [p for i, p in enumerate(corners) if i != missing]
        if _free(g, cells):
            color = colors[placed % len(colors)]
            for r, c in cells:
                g[r][c] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
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
