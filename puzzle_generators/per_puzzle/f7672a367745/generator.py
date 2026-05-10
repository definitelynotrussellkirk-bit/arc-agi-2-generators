"""Generator for arc_puzzle_bank_twentyfirst_21_bundle:easy_146_outline_rectangles_from_diagonal_corner_pairs.

Rule: same-color cells at opposite (diagonal) rectangle corners
expand to draw the rectangle outline.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, rectangles, texture.
Degenerates: no_pairs, single_corner, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7672a367745"
VERSION = "1.1.0"
TASK_ID = "f7672a367745"

SUMMARY = "Same-color diagonal corner pairs define rectangle outlines."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "matching cells are opposite rectangle corners",
    "implied rectangles are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_corner", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 2..3", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "= rectangles", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_corners",
                       "valid": "scattered_diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "= rectangles", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c0, r1, c1):
    h, w = len(g), len(g[0])
    if r0 < 0 or c0 < 0 or r1 >= h or c1 >= w:
        return False
    for r in range(max(0, r0 - 1), min(h, r1 + 2)):
        for c in range(max(0, c0 - 1), min(w, c1 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("rectangles", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 14, 18)
        target = ctx.draw_int("rectangles", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 14)
        target = ctx.draw_int("rectangles", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(9, target))
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        rh = rng.randint(3, min(5, h))
        rw = rng.randint(3, min(6, w))
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        r1, c1 = r0 + rh - 1, c0 + rw - 1
        if not _free(g, r0, c0, r1, c1):
            continue
        color = colors[placed % len(colors)]
        corners = [(r0, c0), (r1, c1)] if rng.choice([False, True]) else [(r0, c1), (r1, c0)]
        for r, c in corners:
            g[r][c] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no diagonal corner pairs.
        return g
    if name == "single_corner":
        # Color appears once — rule's "exactly twice" filter excludes;
        # rectangle is undefined.
        g[2][2] = 4
        return g
    if name == "collinear_corners":
        # Same color on the same row or column rather than diagonally
        # — implied rectangle is 1-D, outline collapses to a line.
        g[3][2] = 4; g[3][7] = 4
        return g
    return g
