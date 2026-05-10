"""Generator for arc_additional_puzzle_bank_volume2:M12: extract the holed object.

Rule: exactly one object has an enclosed hole; that object is normalized
to top-left on a blank output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_distractors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_holed, multiple_holed, all_holed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ff8a4ca30ba"
VERSION = "1.1.0"
TASK_ID = "0ff8a4ca30ba"
SUMMARY = "Exactly one object has an enclosed hole; that object is normalized to top-left on blank output."
INVARIANTS = [
    "one color object is a hollow frame with an internal background hole",
    "other nonzero objects are solid and hole-free",
    "all objects are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_holed", "multiple_holed", "all_holed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..15"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distractors":  {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "frame_with_solid_distractors",
                       "valid": "frame_with_solid_distractors"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


FRAME = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
]
SOLID = [
    [1, 1],
    [1, 1],
]


def _can_place(grid, pattern, top, left):
    h = len(grid)
    w = len(grid[0])
    ph = len(pattern)
    pw = len(pattern[0])
    if top < 1 or left < 1 or top + ph >= h or left + pw >= w:
        return False
    for r in range(top - 1, top + ph + 1):
        for c in range(left - 1, left + pw + 1):
            if grid[r][c] != 0:
                return False
    return True


def _stamp(grid, pattern, top, left, color):
    for rr, row in enumerate(pattern):
        for cc, bit in enumerate(row):
            if bit:
                grid[top + rr][left + cc] = color


def _place(grid, pattern, color, rng):
    h = len(grid)
    w = len(grid[0])
    ph = len(pattern)
    pw = len(pattern[0])
    spots = [
        (r, c)
        for r in range(1, h - ph)
        for c in range(1, w - pw)
        if _can_place(grid, pattern, r, c)
    ]
    if not spots:
        return False
    top, left = rng.choice(spots)
    _stamp(grid, pattern, top, left, color)
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_distractors = ctx.draw_int("n_distractors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n_distractors = ctx.draw_int("n_distractors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        n_distractors = ctx.draw_int("n_distractors", 1, 3)
    colors = list(ctx.draw_distinct_colors("colors", n=4, exclude={0}))
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    _place(g, FRAME, colors[0], rng)
    for i in range(n_distractors):
        _place(g, SOLID, colors[(i + 1) % len(colors)], rng)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_holed":
        # only solid distractors → no frame, rule has nothing to extract, undefined output
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(5, 7):
            for c in range(7, 9): g[r][c] = 6
        return g
    if name == "multiple_holed":
        # two frames → "the holed object" is ambiguous, rule must tie-break or fail
        for (r, c) in [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4)]:
            g[r][c] = 4
        for (r, c) in [(5, 6), (5, 7), (5, 8), (5, 9), (6, 6), (6, 9), (7, 6), (7, 7), (7, 8), (7, 9)]:
            g[r][c] = 6
        return g
    if name == "all_holed":
        # three frames, no solids → all are holed, rule has no unique extract
        for (r, c) in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]: g[r][c] = 4
        for (r, c) in [(1, 6), (1, 7), (1, 8), (2, 6), (2, 8), (3, 6), (3, 7), (3, 8)]: g[r][c] = 6
        for (r, c) in [(6, 3), (6, 4), (6, 5), (7, 3), (7, 5), (8, 3), (8, 4), (8, 5)]: g[r][c] = 8
        return g
    return g
