"""Generator for arc_puzzle_bank_21_set3:S3_E2.

Rule: the leftmost yellow object is recolored green.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_right,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_left_object, no_right_objects, tied_leftmost.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "691d467ddb4d"
VERSION = "1.1.0"
TASK_ID = "691d467ddb4d"

SUMMARY = "The leftmost yellow object is recolored green."

INVARIANTS = [
    "background is 0",
    "all objects are yellow",
    "exactly one object's bounding box has the smallest left column",
    "the selected object remains in place and changes color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_left_object", "no_right_objects", "tied_leftmost")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_right":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "leftmost_plus_right_distractors",
                       "valid": "leftmost_plus_right_distractors"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2)],
]


def _paint(g, cells, r0, c0):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = 4


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    left_shape = rng.choice(_SHAPES)
    left_h = max(r for r, _ in left_shape) + 1
    left_c = rng.randint(0, 1)
    _paint(g, left_shape, rng.randint(1, h - left_h - 1), left_c)
    for _ in range(2):
        cells = rng.choice(_SHAPES)
        max_c = max(c for _, c in cells)
        for _attempt in range(300):
            c0 = rng.randint(max(left_c + max_c + 4, w // 2), w - max_c - 1)
            r0 = rng.randint(1, h - max(r for r, _ in cells) - 2)
            placed = [(r0 + r, c0 + c) for r, c in cells]
            if all(g[r][c] == 0 for r, c in placed):
                _paint(g, cells, r0, c0)
                break
        else:
            raise ValueError("could not place right yellow object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_left_object":
        # only right-side objects → no leftmost to recolor; rule's selection ambiguous
        for (r, c) in [(2, 6), (2, 7), (3, 6)]: g[r][c] = 4
        for (r, c) in [(5, 8), (6, 8), (6, 9)]: g[r][c] = 4
        return g
    if name == "no_right_objects":
        # only one object on left → it is leftmost, gets recolored; weakly tests rule
        for (r, c) in [(3, 1), (3, 2), (4, 1)]: g[r][c] = 4
        return g
    if name == "tied_leftmost":
        # two objects share the same min column → tie-breaking ambiguous
        for (r, c) in [(2, 1), (2, 2), (3, 1)]: g[r][c] = 4
        for (r, c) in [(5, 1), (6, 1), (6, 2)]: g[r][c] = 4  # both start at col 1
        for (r, c) in [(2, 7), (3, 7), (3, 8)]: g[r][c] = 4
        return g
    return g
