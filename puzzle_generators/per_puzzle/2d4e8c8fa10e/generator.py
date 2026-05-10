"""Generator for arc_puzzle_bank_21_set2:S2_E7 — keep only solid 2x2 magenta squares.

Rule: only solid magenta 2x2 square objects survive; other magenta
shapes are erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, square_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_squares, all_squares, no_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "2d4e8c8fa10e"
VERSION = "1.1.0"
TASK_ID = "2d4e8c8fa10e"

SUMMARY = "Only solid magenta 2x2 square objects survive; other magenta shapes are erased."

INVARIANTS = [
    "background is 0",
    "all input objects are magenta",
    "at least one object is a solid 2x2 square",
    "other magenta components are not solid 2x2 squares",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_squares", "all_squares", "no_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "square_count":   {"type": "int", "default": "rng 1..2", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "squares_with_distractors",
                       "valid": "squares_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SQUARE = [(0, 0), (0, 1), (1, 0), (1, 1)]
_OTHER = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        square_count = ctx.draw_int("square_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        square_count = ctx.draw_int("square_count", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        square_count = ctx.draw_int("square_count", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [_SQUARE for _ in range(square_count)]
    shapes.extend(rng.choice(_OTHER) for _ in range(rng.randint(1, 2)))
    rng.shuffle(shapes)
    for cells in shapes:
        if place_no_overlap(rng, g, cells, 6, padding=1, max_tries=400) is None:
            raise ValueError("could not place magenta object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_squares":
        # only non-square shapes → rule erases everything
        for r, c in [(1, 1), (1, 2), (1, 3)]: g[r][c] = 6   # tromino
        for r, c in [(5, 5), (6, 5), (6, 6)]: g[r][c] = 6   # L
        return g
    if name == "all_squares":
        # only solid squares → rule is identity (no distractor erased)
        for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 6
        for r, c in [(5, 5), (5, 6), (6, 5), (6, 6)]: g[r][c] = 6
        return g
    if name == "no_distractors":
        # blank → no objects at all
        return g
    return g
