"""Generator for arc_puzzle_bank_21_set14_s:S14_H7.

The blue object's row profile and red object's column profile define a
canonical intersection grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, profile_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blue, no_red, zero_profiles.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4238cc89338a"
VERSION = "1.1.0"
TASK_ID = "4238cc89338a"
SUMMARY = "Build the 8-intersection grid from blue row counts and red column counts."

INVARIANTS = [
    "one color-1 object provides a row-count profile",
    "one color-2 object provides a column-count profile",
    "both profiles contain positive counts",
    "the output is the canonical intersection of those two profiles",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blue", "no_red", "zero_profiles")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "profile_variant": {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "blue_rows_red_cols",
                       "valid": "blue_rows_red_cols"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PROFILES = [
    ([1, 3, 2], [2, 1, 3]),
    ([2, 2, 1], [1, 3, 1]),
    ([3, 1, 2], [2, 2, 2]),
]


def _paint_rows(g, top, left, profile, color):
    for r, count in enumerate(profile):
        for c in range(count):
            g[top + r][left + c] = color


def _paint_cols(g, top, left, profile, color):
    for c, count in enumerate(profile):
        for r in range(count):
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
    if difficulty == "easy":
        profile_idx = ctx.draw_int("profile_variant", 0, 0)
    elif difficulty == "hard":
        profile_idx = ctx.draw_int("profile_variant", 0, len(_PROFILES) - 1)
    else:
        profile_idx = ctx.draw_int("profile_variant", 0, len(_PROFILES) - 1)
    row_profile, col_profile = _PROFILES[profile_idx]
    g = full_grid(9, 12, 0)
    blue_top = 1 + rng.randint(0, 1)
    blue_left = 1 + rng.randint(0, 1)
    red_top = 1 + rng.randint(0, 1)
    red_left = 7 + rng.randint(0, 1)
    _paint_rows(g, blue_top, blue_left, row_profile, 1)
    _paint_cols(g, red_top, red_left, col_profile, 2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_blue":
        # red profile only → no row counts to define rows
        _paint_cols(g, 2, 7, [2, 1, 3], 2)
        return g
    if name == "no_red":
        # blue profile only → no column counts to define cols
        _paint_rows(g, 2, 1, [1, 3, 2], 1)
        return g
    if name == "zero_profiles":
        # both objects have only 1 cell → degenerate single-cell intersection
        g[2][2] = 1
        g[2][8] = 2
        return g
    return g
