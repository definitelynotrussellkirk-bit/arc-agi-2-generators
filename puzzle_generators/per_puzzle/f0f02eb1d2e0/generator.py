"""Generator for arc_puzzle_bank_tenth21:E67.

Three same-color rectangle corners imply the missing fourth corner.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, full_4_corners, line_only_three.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f0f02eb1d2e0"
VERSION = "1.1.0"
TASK_ID = "f0f02eb1d2e0"

SUMMARY = "Three same-color rectangle corners imply the missing fourth corner."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly three times",
    "the three cells occupy two rows and two columns",
    "the missing rectangle corner is initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "full_4_corners", "line_only_three")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "three_corner_rects",
                       "valid": "three_corner_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        target = ctx.draw_int("n_rects", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("n_rects", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(colors)
    used: set[tuple[int, int]] = set()
    placed = 0
    for color in colors:
        if placed >= target:
            break
        for _ in range(100):
            r0, r1 = sorted(rng.sample(range(h), 2))
            c0, c1 = sorted(rng.sample(range(w), 2))
            corners = [(r0, c0), (r0, c1), (r1, c0), (r1, c1)]
            if any(p in used for p in corners):
                continue
            missing = rng.choice(corners)
            for r, c in corners:
                if (r, c) != missing:
                    g[r][c] = color
            used.update(corners)
            placed += 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no triple-corner sets to complete
        return g
    if name == "full_4_corners":
        # all 4 corners present → no missing corner
        for r, c in [(1, 1), (1, 7), (5, 1), (5, 7)]:
            g[r][c] = 4
        return g
    if name == "line_only_three":
        # 3 cells colinear (one row or one col) → not 2 rows × 2 cols, fails
        for c in [1, 4, 7]: g[3][c] = 4
        return g
    return g
