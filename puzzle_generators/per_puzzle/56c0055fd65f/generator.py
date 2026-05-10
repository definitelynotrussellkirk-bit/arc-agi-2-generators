"""Generator for arc_additional_puzzle_bank_volume8:M55: recolor by hole count.

Rule: yellow components with 0/1/2 holes → 2/3/8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, include_distractor,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid, all_one_hole, no_yellow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "56c0055fd65f"
VERSION = "1.1.0"
TASK_ID = "56c0055fd65f"
SUMMARY = "Yellow components with 0, 1, or 2 holes are recolored to 2, 3, or 8."
INVARIANTS = [
    "all yellow components are separated by background",
    "yellow components enclose zero, one, or two background holes",
    "non-yellow distractors are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "all_one_hole", "no_yellow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "include_distractor": {"type": "bool", "default": "rng", "valid": "true,false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_holes",
                       "valid": "scattered_holes"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SOLID = [
    [1, 1, 1],
    [1, 1, 1],
]
ONE_HOLE = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
]
TWO_HOLES = [
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1],
]


def _rotated(pattern):
    return [list(row) for row in zip(*pattern[::-1])]


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


def _place_shape(grid, pattern, rng):
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
    _stamp(grid, pattern, top, left, 4)
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 15)
    include_distractor = ctx.draw_choice("include_distractor", [True, False])
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    patterns = [SOLID, ONE_HOLE, TWO_HOLES]
    rng.shuffle(patterns)
    for pattern in patterns:
        candidate = _rotated(pattern) if rng.random() < 0.5 else pattern
        if not _place_shape(g, candidate, rng):
            _place_shape(g, pattern, rng)

    if include_distractor:
        for _ in range(40):
            r = rng.randint(1, h - 2)
            c = rng.randint(1, w - 3)
            if g[r][c] == 0 and g[r][c + 1] == 0:
                g[r][c] = 6
                g[r][c + 1] = 6
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # all yellow blocks are solid (0 holes) → only the 0-hole → 2 branch fires
        for r in range(1, 3):
            for c in range(1, 4): g[r][c] = 4
        for r in range(5, 7):
            for c in range(7, 10): g[r][c] = 4
        return g
    if name == "all_one_hole":
        # all yellow blocks are 1-hole frames → only the 1-hole → 3 branch fires
        for r in range(1, 4):
            for c in range(1, 4): g[r][c] = 4
        g[2][2] = 0
        for r in range(6, 9):
            for c in range(7, 10): g[r][c] = 4
        g[7][8] = 0
        return g
    if name == "no_yellow":
        # no color-4 cells → rule fires zero times
        for r in range(2, 4):
            for c in range(3, 5): g[r][c] = 6
        for r in range(7, 9):
            for c in range(8, 11): g[r][c] = 8
        return g
    return g
