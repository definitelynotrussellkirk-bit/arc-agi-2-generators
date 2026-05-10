"""Generator for arc_puzzle_bank_21_set14_s:S14_M1.

Rule: a blue anchor's row-count profile identifies the matching
non-blue object to crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_shift,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_match, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "3d856836c655"
VERSION = "1.1.0"
TASK_ID = "3d856836c655"
SUMMARY = "A blue anchor's row-count profile identifies the matching non-blue object to crop."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue anchor object",
    "one non-blue target has the same row profile as the anchor",
    "other objects have different row profiles",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_match", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..15"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_shift":   {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "anchor_left",
                       "valid": "anchor_left"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

PLUS_PROFILE = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
ODD_PROFILE = [(0, 0), (0, 1), (1, 1), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 15, 16)
    else:
        h = ctx.draw_int("height", 10, 12)
        w = ctx.draw_int("width", 13, 16)
    shift = ctx.draw_int("target_shift", 0, 1)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r0 = rng.randint(1, 2)
    paint_at(g, r0, 1, PLUS_PROFILE, 1)
    paint_at(g, r0, 6 + shift, PLUS_PROFILE, 4)
    paint_at(g, h - 4, w - 4, ODD_PROFILE, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # no blue anchor → no profile to match against
        paint_at(g, 1, 6, PLUS_PROFILE, 4)
        paint_at(g, h - 4, w - 4, ODD_PROFILE, 6)
        return g
    if name == "no_match":
        # anchor exists but no non-blue object shares its profile → match undefined
        paint_at(g, 1, 1, PLUS_PROFILE, 1)
        paint_at(g, 1, 6, ODD_PROFILE, 4)
        paint_at(g, h - 4, w - 4, ODD_PROFILE, 6)
        return g
    if name == "all_match":
        # every non-blue object shares the anchor's profile → tie, target ambiguous
        paint_at(g, 1, 1, PLUS_PROFILE, 1)
        paint_at(g, 1, 6, PLUS_PROFILE, 4)
        paint_at(g, h - 4, w - 4, PLUS_PROFILE, 6)
        return g
    return g
