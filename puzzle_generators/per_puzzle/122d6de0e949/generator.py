"""Generator for arc_puzzle_bank_21_set14_s:S14_H4.

The color-1 anchor contributes a column-count profile. The target object is
the first non-anchor component whose row profile is the reversed anchor column
profile.

Combinatorial axes (8): grid_h, grid_w, palette_kind, profile_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_target_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "122d6de0e949"
VERSION = "1.1.0"
TASK_ID = "122d6de0e949"
SUMMARY = "Find the object whose row profile reverses the anchor column profile."

INVARIANTS = [
    "one color-1 anchor object has a nonuniform column profile",
    "exactly one non-anchor object has the reversed profile as its row profile",
    "distractors have different row profiles",
    "the selected object is cropped and recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_target_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "profile_variant":{"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "anchor_plus_target_plus_distractor",
                       "valid": "anchor_plus_target_plus_distractor"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_ANCHOR_COLS = [
    [1, 3, 2],
    [2, 1, 3],
    [3, 2, 1],
]


def _paint_cols(g, top, left, profile, color):
    for c, count in enumerate(profile):
        for r in range(count):
            g[top + r][left + c] = color


def _paint_rows(g, top, left, profile, color):
    for r, count in enumerate(profile):
        for c in range(count):
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
        anchor_profile = _ANCHOR_COLS[ctx.draw_int("profile_variant", 0, 1)]
    elif difficulty == "hard":
        anchor_profile = _ANCHOR_COLS[ctx.draw_int("profile_variant", 1, 2)]
    else:
        anchor_profile = _ANCHOR_COLS[ctx.draw_int("profile_variant", 0, len(_ANCHOR_COLS) - 1)]
    target_profile = list(reversed(anchor_profile))
    target_color = rng.choice([3, 4, 5, 6, 7, 9])
    g = full_grid(10, 12, 0)

    _paint_cols(g, 1, 1, anchor_profile, 1)
    _paint_rows(g, 5, 6, target_profile, target_color)
    _paint_rows(g, 6, 1, [1, 2, 1], rng.choice([c for c in [3, 4, 5, 6, 7, 9] if c != target_color]))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_anchor":
        # no color-1 anchor → no profile to compute, no selection
        _paint_rows(g, 5, 6, [2, 1, 3], 4)
        _paint_rows(g, 6, 1, [1, 2, 1], 6)
        return g
    if name == "no_target_match":
        # anchor present but no candidate has the reversed profile → no selection
        _paint_cols(g, 1, 1, [1, 3, 2], 1)
        _paint_rows(g, 5, 6, [1, 2, 1], 4)
        _paint_rows(g, 6, 1, [3, 1, 2], 6)
        return g
    if name == "multiple_matches":
        # multiple non-anchor objects share the reversed profile → ambiguous
        _paint_cols(g, 1, 1, [1, 3, 2], 1)
        _paint_rows(g, 5, 6, [2, 3, 1], 4)
        _paint_rows(g, 7, 1, [2, 3, 1], 6)
        return g
    return g
