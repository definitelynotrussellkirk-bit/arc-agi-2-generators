"""Generator for arc_puzzle_bank_21_set6_s:S6_E3.

Rule: two separated objects exchange colors while keeping their shapes fixed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_pair,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_object, identical_colors, more_than_two_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "42a28f889145"
VERSION = "1.1.0"
TASK_ID = "42a28f889145"
SUMMARY = "Two separated objects exchange colors while keeping their shapes fixed."

INVARIANTS = [
    "background is 0",
    "there are exactly two connected nonzero objects",
    "the objects have distinct colors",
    "the two objects are separated left-to-right",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_object", "identical_colors", "more_than_two_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_pair":     {"type": "choice", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "left_right_split",
                       "valid": "left_right_split"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
]


def _paint(g, cells, r0, c0, color):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 10, 14)
    pair = ctx.draw_choice("shape_pair", list(range(len(_SHAPES))))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color_a, color_b = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    left = _SHAPES[pair]
    right = _SHAPES[(pair + rng.randint(1, len(_SHAPES) - 1)) % len(_SHAPES)]
    lh = max(r for r, _ in left) + 1
    lw = max(c for _, c in left) + 1
    rh = max(r for r, _ in right) + 1
    rw = max(c for _, c in right) + 1
    left_r = rng.randint(1, h - lh - 1)
    left_c = rng.randint(1, max(1, w // 3 - lw))
    right_r = rng.randint(1, h - rh - 1)
    right_c = rng.randint(max(left_c + lw + 3, w // 2), w - rw - 1)
    _paint(g, left, left_r, left_c, color_a)
    _paint(g, right, right_r, right_c, color_b)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "single_object":
        # only one object → no swap partner, rule has nothing to exchange
        _paint(g, _SHAPES[0], 2, 4, 5)
        return g
    if name == "identical_colors":
        # both objects same color → swap is identity, rule has no visible effect
        _paint(g, _SHAPES[0], 2, 1, 5)
        _paint(g, _SHAPES[1], 2, 7, 5)
        return g
    if name == "more_than_two_objects":
        # 3+ objects → "exactly two" invariant violated, ambiguous which pair to swap
        _paint(g, _SHAPES[0], 1, 1, 4)
        _paint(g, _SHAPES[1], 1, 6, 5)
        _paint(g, _SHAPES[2], 5, 9, 6)
        return g
    return g
