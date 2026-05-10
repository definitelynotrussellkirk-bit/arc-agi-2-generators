"""Generator for arc_puzzle_bank_21_set9_e:medium_i10 — fill rect by 4 corner markers.

Rule: each color appearing exactly 4 times at the corners of a
rectangle (axis-aligned) → fill the entire rectangle with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, three_corners, collinear_marks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cdf26af5c935"
VERSION = "1.1.0"
TASK_ID = "cdf26af5c935"
SUMMARY = "1-2 colors each at 4 corners of a non-degenerate axis-aligned rectangle."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears exactly 4 times at the 4 corners of a rect",
    "rect bboxes don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "three_corners", "collinear_marks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "4_corners_per_rect",
                       "valid": "4_corners_per_rect"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    reserved: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 4)
            c1 = rng.randint(0, w - 4)
            r2 = rng.randint(r1 + 3, min(h - 1, r1 + 5))
            c2 = rng.randint(c1 + 3, min(w - 1, c1 + 5))
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & reserved:
                continue
            g[r1][c1] = color
            g[r1][c2] = color
            g[r2][c1] = color
            g[r2][c2] = color
            reserved |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangle corners to fill from
        return g
    if name == "three_corners":
        # 3 corners only → "exactly 4" precondition fails
        g[1][1] = 4; g[1][6] = 4; g[5][1] = 4
        return g
    if name == "collinear_marks":
        # 4 marks all on same row → no rectangle, degenerate
        for c in [1, 3, 5, 7]: g[3][c] = 4
        return g
    return g
