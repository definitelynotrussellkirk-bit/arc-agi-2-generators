"""Generator for arc_additional_puzzles_21_set10_bundle:E67 — Fill bbox between 2-cell pairs.

Rule: for each color with exactly 2 cells, paint the rectangle bounded
by those 2 cells in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_marker, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1d23d72f3b43"
VERSION = "1.1.0"
TASK_ID = "1d23d72f3b43"
SUMMARY = "1-3 distinct colors, each with exactly 2 cells (corners of a rectangle)."

INVARIANTS = [
    "1-3 distinct non-bg colors",
    "each color appears exactly 2 times",
    "rectangles for different colors don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_marker", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "scattered_corner_pairs",
                       "valid": "scattered_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_pairs = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_pairs)
    occupied = [[False] * w for _ in range(h)]
    pairs_placed = 0
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 1); c1 = rng.randint(0, w - 1)
            r2 = rng.randint(0, h - 1); c2 = rng.randint(0, w - 1)
            if (r1, c1) == (r2, c2):
                continue
            rmin, rmax = sorted([r1, r2])
            cmin, cmax = sorted([c1, c2])
            if rmax - rmin < 2 or cmax - cmin < 2:
                continue
            if any(occupied[rr][cc] for rr in range(rmin, rmax + 1) for cc in range(cmin, cmax + 1)):
                continue
            for rr in range(rmin, rmax + 1):
                for cc in range(cmin, cmax + 1):
                    occupied[rr][cc] = True
            g[r1][c1] = color
            g[r2][c2] = color
            pairs_placed += 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule's pair-finder finds no color appearing 2x.
        return g
    if name == "single_marker":
        # One color appears once (not twice) — rule's "exactly 2 cells"
        # filter excludes it; nothing to fill.
        g[2][2] = 4
        return g
    if name == "collinear_pair":
        # Pair shares row or column — bbox between them is 1-D, not a
        # rectangle; rule's "fill rectangle" produces a degenerate line.
        g[3][1] = 4; g[3][7] = 4
        return g
    return g
