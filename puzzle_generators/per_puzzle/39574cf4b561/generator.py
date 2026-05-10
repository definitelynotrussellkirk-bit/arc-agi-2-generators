"""Generator for arc_additional_puzzle_bank_volume9:E61 — infer 4th rectangle corner.

Rule: each color has 3 of 4 axis-aligned rectangle corners; the
missing fourth corner is added.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangles, complete_rect, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "39574cf4b561"
VERSION = "1.1.0"
TASK_ID = "39574cf4b561"
SUMMARY = "Each color has three rectangle corners; the missing fourth corner is added."

INVARIANTS = [
    "background is 0",
    "each active nonzero color appears exactly three times",
    "the three cells are corners of one axis-aligned rectangle",
    "rectangles for different colors do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "complete_rect", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rectangles":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "= n_rectangles", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "non_overlapping_3corner_rects",
                       "valid": "non_overlapping_3corner_rects"},
    "n_distinct_colors": {"type": "int", "default": "= n_rectangles", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_rectangles = ctx.draw_int("n_rectangles", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 13, 18)
        n_rectangles = ctx.draw_int("n_rectangles", 4, 7)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_rectangles = ctx.draw_int("n_rectangles", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    colors = list(range(1, 10))
    rng.shuffle(colors)
    placed = 0
    used: set[tuple[int, int]] = set()
    for color in colors:
        if placed >= n_rectangles:
            break
        for _ in range(80):
            r1, r2 = sorted(rng.sample(range(h), 2))
            c1, c2 = sorted(rng.sample(range(w), 2))
            if r2 - r1 < 2 or c2 - c1 < 2:
                continue
            corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
            if any(p in used for p in corners):
                continue
            missing = rng.choice(corners)
            for r, c in corners:
                if (r, c) != missing:
                    g[r][c] = color
            used.update(corners)
            placed += 1
            break
    if placed == 0:
        g[1][1] = 1
        g[1][4] = 1
        g[4][1] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # Empty grid — no 3 corners to extrapolate.
        return g
    if name == "complete_rect":
        # All 4 corners present — rule has nothing to add.
        for r, c in [(1, 1), (1, 5), (5, 1), (5, 5)]:
            g[r][c] = 4
        return g
    if name == "collinear_corners":
        # Three same-color cells on the same row — they aren't 3 of 4
        # rectangle corners, so the rule's inference is undefined.
        g[3][1] = 4; g[3][4] = 4; g[3][7] = 4
        return g
    return g
