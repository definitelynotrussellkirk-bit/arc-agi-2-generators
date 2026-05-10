"""Generator for arc_puzzle_bank_21_set21_bundle:easy_p04.

Three same-color rectangle corners are present and the fourth corner is blank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, full_4_corners, two_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c24bb478ceb4"
VERSION = "1.1.0"
TASK_ID = "c24bb478ceb4"
SUMMARY = "Three same-color rectangle corners are present and the fourth corner is blank."

INVARIANTS = [
    "background is 0",
    "each color appears in exactly three corners of one rectangle",
    "rectangles use distinct colors and do not share corner cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "full_4_corners", "two_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "three_corners_per_rect",
                       "valid": "three_corners_per_rect"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        rectangle_count = ctx.draw_int("rectangle_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        rectangle_count = ctx.draw_int("rectangle_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        rectangle_count = ctx.draw_int("rectangle_count", 2, 3)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], rectangle_count)

    attempts = 0
    placed = 0
    while placed < rectangle_count and attempts < 200:
        attempts += 1
        r0, r1 = sorted(rng.sample(range(h), 2))
        c0, c1 = sorted(rng.sample(range(w), 2))
        corners = [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]
        if any(p in used for p in corners):
            continue
        missing = rng.choice(corners)
        color = colors[placed]
        for r, c in corners:
            if (r, c) != missing:
                grid[r][c] = color
        used.update(corners)
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to complete the 4th corner of
        return g
    if name == "full_4_corners":
        # all 4 corners present → no missing corner to fill
        for r, c in [(1, 1), (1, 6), (5, 1), (5, 6)]: g[r][c] = 4
        return g
    if name == "two_corners":
        # only 2 corners → "exactly three" precondition fails
        g[1][1] = 4; g[5][6] = 4
        return g
    return g
