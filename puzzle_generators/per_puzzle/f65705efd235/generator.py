"""Generator for arc_additional_puzzles_21_set9:E60 — Draw rect outline from 4 corner cells.

Rule: for each color appearing as 4 cells forming a rectangle's
corners, draw the full outline.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corners, partial_corners, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f65705efd235"
VERSION = "1.1.0"
TASK_ID = "f65705efd235"
SUMMARY = "1-2 colors, each with 4 cells at corners of a rectangle ≥3×3."

INVARIANTS = [
    "1-2 distinct non-bg colors",
    "each color: 4 cells at distinct rectangle corners with bbox ≥3×3",
    "rectangles don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "partial_corners", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "4_corner_pairs_per_color",
                       "valid": "4_corner_pairs_per_color"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_rects = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_rects)
    occupied = [[False] * w for _ in range(h)]
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 4); c1 = rng.randint(0, w - 4)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 5))
            c2 = rng.randint(c1 + 2, min(w - 1, c1 + 5))
            corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
            if any(occupied[r][c] for r, c in corners):
                continue
            for r, c in corners:
                g[r][c] = color
                occupied[r][c] = True
            # Mark interior as occupied so other rects don't overlap
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    occupied[r][c] = True
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # blank → no corners to interpret as rectangles
        return g
    if name == "partial_corners":
        # only 2 or 3 corners per color → can't define a rectangle
        g[1][1] = 4; g[1][6] = 4; g[5][1] = 4
        return g
    if name == "collinear_corners":
        # 4 cells but all in same row/col → degenerate to a line, not a rect
        g[3][1] = 4; g[3][3] = 4; g[3][6] = 4; g[3][8] = 4
        return g
    return g
