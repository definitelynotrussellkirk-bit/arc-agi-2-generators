"""Generator for arc_puzzle_bank_21_set14_s:S14_H5 — abs-diff of row profiles → cyan histogram.

Rule: compute the absolute difference between two object row profiles
as a cyan histogram.

Combinatorial axes (8): grid_h, grid_w, palette_kind, profile,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, no_left_object, no_right_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dcfb4c64c914"
VERSION = "1.1.0"
TASK_ID = "dcfb4c64c914"
SUMMARY = "Compute the absolute difference between two object row profiles as a cyan histogram."

INVARIANTS = [
    "one full color-5 column splits the grid into two panels",
    "each panel contains exactly one connected nonzero object",
    "the objects are row-left-justified profile shapes",
    "the output is the left-justified cyan histogram of absolute row-profile differences",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "no_left_object", "no_right_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "profile":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_panels_with_separator",
                       "valid": "two_panels_with_separator"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PROFILE_PAIRS = [
    ([1, 3, 2], [3, 1, 1]),
    ([3, 2, 1], [1, 1, 3]),
    ([2, 4, 1], [1, 2, 3]),
    ([1, 2, 3, 2], [3, 1, 1]),
    ([4, 1, 3], [2, 3, 1, 2]),
    ([2, 1, 4, 3], [1, 3, 2, 1]),
]


def _paint_profile(g, top, left, profile, color):
    for r, count in enumerate(profile):
        for c in range(count):
            g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("profile", 0, 2)
    elif difficulty == "hard":
        idx = ctx.draw_int("profile", 3, 5)
    else:
        idx = ctx.draw_int("profile", 0, len(_PROFILE_PAIRS) - 1)
    left_profile, right_profile = _PROFILE_PAIRS[idx]
    colors = rng.sample([1, 2, 3, 4, 6, 7, 9], 2)
    g = full_grid(8, 15, 0)
    for r in range(8):
        g[r][7] = 5
    _paint_profile(g, 2, 1, left_profile, colors[0])
    _paint_profile(g, 2, 9, right_profile, colors[1])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 15, 0)
    if name == "no_separator":
        # both panels filled but no 5-divider → cannot split
        _paint_profile(g, 2, 1, _PROFILE_PAIRS[0][0], 4)
        _paint_profile(g, 2, 9, _PROFILE_PAIRS[0][1], 6)
        return g
    if name == "no_left_object":
        # separator + right object only → no left profile to subtract
        for r in range(8): g[r][7] = 5
        _paint_profile(g, 2, 9, _PROFILE_PAIRS[0][1], 6)
        return g
    if name == "no_right_object":
        # separator + left object only → no right profile to subtract
        for r in range(8): g[r][7] = 5
        _paint_profile(g, 2, 1, _PROFILE_PAIRS[0][0], 4)
        return g
    return g
