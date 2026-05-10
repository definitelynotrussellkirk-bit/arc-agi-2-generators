"""Generator for arc_puzzle_bank_21_set14_s:S14_H2.

Rule: blue object's row profile + red object's column profile select a
candidate object that matches both; recolor it 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blue_profile, no_red_profile, no_matching_candidate.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0eb4eaa46003"
VERSION = "1.1.0"
TASK_ID = "0eb4eaa46003"
SUMMARY = "Select the object whose row profile matches blue and column profile matches red."

INVARIANTS = [
    "one color-1 object defines the target row profile",
    "one color-2 object defines the target column profile",
    "exactly one non-1/non-2 object matches both profiles",
    "the selected object is cropped and recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blue_profile", "no_red_profile", "no_matching_candidate")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "profile_variant": {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_profiles_with_candidates",
                       "valid": "two_profiles_with_candidates"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TARGETS = [
    [[1, 1, 0], [1, 1, 1], [0, 0, 1]],
    [[1, 0, 0], [1, 1, 1], [1, 1, 0]],
]


def _row_profile(shape):
    return [sum(row) for row in shape]


def _col_profile(shape):
    return [sum(row[c] for row in shape) for c in range(len(shape[0]))]


def _paint_rows(g, top, left, profile, color):
    for r, count in enumerate(profile):
        for c in range(count):
            g[top + r][left + c] = color


def _paint_cols(g, top, left, profile, color):
    for c, count in enumerate(profile):
        for r in range(count):
            g[top + r][left + c] = color


def _paint_shape(g, top, left, shape, color):
    for r, row in enumerate(shape):
        for c, v in enumerate(row):
            if v:
                g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    shape = _TARGETS[ctx.draw_int("profile_variant", 0, len(_TARGETS) - 1)]
    target_color = rng.choice([3, 4, 5, 6, 7, 9])
    g = full_grid(10, 13, 0)

    _paint_rows(g, 1, 1, _row_profile(shape), 1)
    _paint_cols(g, 1, 7, _col_profile(shape), 2)
    _paint_shape(g, 5, 4, shape, target_color)
    _paint_shape(g, 6, 10, [[1, 1], [1, 0]], rng.choice([c for c in [3, 4, 5, 6, 7, 9] if c != target_color]))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 13, 0)
    shape = _TARGETS[0]
    if name == "no_blue_profile":
        # No blue object — rule's row-profile selector has no input.
        _paint_cols(g, 1, 7, _col_profile(shape), 2)
        _paint_shape(g, 5, 4, shape, 4)
        _paint_shape(g, 6, 10, [[1, 1], [1, 0]], 6)
        return g
    if name == "no_red_profile":
        # No red object — rule's column-profile selector has no input.
        _paint_rows(g, 1, 1, _row_profile(shape), 1)
        _paint_shape(g, 5, 4, shape, 4)
        _paint_shape(g, 6, 10, [[1, 1], [1, 0]], 6)
        return g
    if name == "no_matching_candidate":
        # Profiles present but no candidate object matches —
        # rule's selection branch yields no result.
        _paint_rows(g, 1, 1, _row_profile(shape), 1)
        _paint_cols(g, 1, 7, _col_profile(shape), 2)
        _paint_shape(g, 6, 10, [[1, 1], [1, 0]], 4)
        _paint_shape(g, 5, 4, [[1, 1, 1], [0, 1, 0]], 6)
        return g
    return g
