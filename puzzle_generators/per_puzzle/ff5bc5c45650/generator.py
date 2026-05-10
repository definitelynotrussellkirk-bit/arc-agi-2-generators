"""Generator for arc_puzzle_bank_21_set14_s:S14_M5.

Rule: largest object's row and column profiles are intersected into a
canonical cyan-on-zero mask of the object's bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, include_distractor,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, no_objects, profile_solid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ff5bc5c45650"
VERSION = "1.1.0"
TASK_ID = "ff5bc5c45650"
SUMMARY = "One uniquely-largest profile object plus optional smaller distractor."

INVARIANTS = [
    "background is 0",
    "one object is uniquely largest by cell count",
    "the largest object has nontrivial row and column profiles",
    "distractors are smaller and do not affect the profile source",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "no_objects", "profile_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

PROFILE_SHAPE = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)]
SMALL_L = [(0, 0), (1, 0), (1, 1)]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "include_distractor": {"type": "bool", "default": "rng",
                           "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "top_band",
                       "valid": "top_band"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
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
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 11, 12)
        include_distractor = ctx.draw_choice("include_distractor", [False])
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 13, 14)
        include_distractor = ctx.draw_choice("include_distractor", [True])
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 11, 14)
        include_distractor = ctx.draw_choice("include_distractor", [False, True])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    paint_at(g, rng.randint(1, 2), 2, PROFILE_SHAPE, 3)
    if include_distractor:
        paint_at(g, h - 3, w - 4, SMALL_L, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # two objects of equal cell count → no unique "largest", rule ambiguous
        paint_at(g, 1, 2, PROFILE_SHAPE, 3)
        paint_at(g, 6, 7, PROFILE_SHAPE, 6)
        return g
    if name == "no_objects":
        # empty grid → no profile source, rule has no anchor
        return g
    if name == "profile_solid":
        # largest object is a solid rectangle → profile intersection = the bbox
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 3
        paint_at(g, h - 3, w - 4, SMALL_L, 6)
        return g
    return g
