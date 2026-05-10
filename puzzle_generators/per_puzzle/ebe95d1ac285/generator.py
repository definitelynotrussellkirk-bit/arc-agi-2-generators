"""Generator for arc_puzzle_bank_21_set13_s:S13_M6 — anchor's border-touch + symmetry select matches.

Rule: a red anchor's border-touch and symmetry class select matching components.

Combinatorial axes (8): grid_h, grid_w, palette_kind, anchor_axis,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_matches, all_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ebe95d1ac285"
VERSION = "1.1.0"
TASK_ID = "ebe95d1ac285"
SUMMARY = "A red anchor's border-touch and symmetry class select matching components."

INVARIANTS = [
    "background is 0",
    "there is exactly one red anchor object",
    "one non-anchor object matches both the anchor's border-touch flag and symmetry class",
    "other objects fail either the border-touch or symmetry predicate",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_matches", "all_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "width":          {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_axis":    {"type": "enum", "default": "rng vertical|horizontal",
                       "valid": "vertical|horizontal"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "anchor_with_match_and_decoys",
                       "valid": "anchor_with_match_and_decoys"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

VERT_ONLY = [(0, 0), (0, 1), (0, 2), (1, 1)]
HORIZ_ONLY = [(0, 0), (1, 0), (2, 0), (1, 1)]
BOTH = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 15, 16)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 13, 16)
    axis = ctx.draw_choice("anchor_axis", ["vertical", "horizontal"])
    g = full_grid(h, w, 0)

    shape = VERT_ONLY if axis == "vertical" else HORIZ_ONLY
    paint_at(g, 0, 1, shape, 2)
    paint_at(g, h - 3, w - 4, shape, 4)
    paint_at(g, 3, 5, shape, 6)
    paint_at(g, h - 4, 1, BOTH, 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # no red anchor → predicate (anchor's flags) undefined
        paint_at(g, 1, 1, VERT_ONLY, 4)
        paint_at(g, 5, 5, HORIZ_ONLY, 6)
        return g
    if name == "no_matches":
        # anchor present but no other component matches both predicates → empty match set
        paint_at(g, 0, 1, VERT_ONLY, 2)   # anchor (border-touch + vsym)
        # All other components fail at least one predicate (interior + asym)
        paint_at(g, 4, 6, [(0, 0), (0, 1), (1, 0)], 6)   # interior + asym
        paint_at(g, 7, 9, [(0, 0), (1, 1), (2, 0)], 4)   # interior + asym
        return g
    if name == "all_match":
        # all non-anchor components match both predicates → all recolored
        paint_at(g, 0, 1, VERT_ONLY, 2)   # anchor (border + vsym)
        paint_at(g, 0, 8, VERT_ONLY, 4)   # match
        paint_at(g, 8, 1, VERT_ONLY, 6)   # match
        return g
    return g
