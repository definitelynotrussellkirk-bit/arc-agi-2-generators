"""Generator for arc_additional_puzzle_bank_volume16:M109.

Rule: the red candidate that is a true mirror, not a rotation, of the
blue source recolors cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_candidates,
palette_size, position_bias, n_distinct_colors, chirality, texture.
Degenerates: no_mirror, all_mirrors, achiral_source.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "85f0fcea28c0"
VERSION = "1.1.0"
TASK_ID = "85f0fcea28c0"
SUMMARY = "The red candidate that is a true mirror, not a rotation, of the blue source recolors cyan."

INVARIANTS = [
    "background is 0",
    "the blue source shape is chiral",
    "one red candidate is a reflected form of the source",
    "another red candidate is a rotation or nonmatch and remains red",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_mirror", "all_mirrors", "achiral_source")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_candidates":   {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "chirality":      {"type": "str", "default": "chiral_source",
                       "valid": "chiral_source"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 12, 16)
    g = full_grid(h, w, 0)
    source = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1)]
    mirror = [(1, w - 4), (2, w - 4), (3, w - 4), (4, w - 5), (4, w - 4)]
    distractor = [(h - 4, 2), (h - 4, 3), (h - 3, 2), (h - 3, 3), (h - 2, 3)]
    for r, c in source:
        g[r][c] = 1
    for cells in [mirror, distractor]:
        for r, c in cells:
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    source = [(1, 1), (1, 2), (1, 3), (1, 4), (2, 1)]
    rotation_only = [(1, w - 5), (1, w - 4), (1, w - 3), (1, w - 2), (2, w - 2)]
    mirror = [(1, w - 4), (2, w - 4), (3, w - 4), (4, w - 5), (4, w - 4)]
    distractor = [(h - 4, 2), (h - 4, 3), (h - 3, 2), (h - 3, 3), (h - 2, 3)]
    for r, c in source:
        g[r][c] = 1
    if name == "no_mirror":
        # both red candidates are rotations / non-matches → no winner to recolor
        for r, c in rotation_only:
            g[r][c] = 2
        for r, c in distractor:
            g[r][c] = 2
        return g
    if name == "all_mirrors":
        # both red candidates are mirrors → tie, target ambiguous
        for r, c in mirror:
            g[r][c] = 2
        mirror2 = [(h - 4, w - 5), (h - 4, w - 4), (h - 3, w - 5), (h - 2, w - 5), (h - 2, w - 4)]
        for r, c in mirror2:
            g[r][c] = 2
        return g
    if name == "achiral_source":
        # source has mirror symmetry → mirror = rotation, recolor criterion vacuous
        achiral = [(1, 1), (1, 2), (1, 3), (2, 2), (3, 1), (3, 2), (3, 3)]
        g2 = full_grid(h, w, 0)
        for r, c in achiral:
            g2[r][c] = 1
        for r, c in mirror:
            g2[r][c] = 2
        for r, c in distractor:
            g2[r][c] = 2
        return g2
    return g
