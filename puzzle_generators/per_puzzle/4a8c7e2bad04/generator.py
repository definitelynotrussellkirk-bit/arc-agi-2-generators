"""Generator for arc_puzzle_bank_21_set8_s:S8_H4 — match by row-occupancy signature.

Rule: match the non-query object with the same per-row occupancy
signature.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_query, no_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a8c7e2bad04"
VERSION = "1.1.0"
TASK_ID = "4a8c7e2bad04"
SUMMARY = "Match the non-query object with the same per-row occupancy signature."

INVARIANTS = [
    "one query object is color 8",
    "one non-query object has the same row-count signature as the query",
    "a distractor object has a different row-count signature",
    "the output is the cropped matching object with its original color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_query", "no_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "query_with_match_and_distractor",
                       "valid": "query_with_match_and_distractor"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
]
_DISTRACTORS = [
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("shape", 0, 0)
    elif difficulty == "hard":
        idx = ctx.draw_int("shape", 1, 2)
    else:
        idx = ctx.draw_int("shape", 0, 2)
    match_color = rng.choice([2, 3, 4, 5, 6, 7, 9])
    distractor_color = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 9] if c != match_color])
    g = full_grid(9, 14, 0)
    _paint(g, 1, 1, _SHAPES[idx], 8)
    _paint(g, 1, 8, _SHAPES[idx], match_color)
    _paint(g, 5, 3, _DISTRACTORS[idx], distractor_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 14, 0)
    if name == "no_query":
        # match + distractor present but no color-8 query → no signature anchor
        _paint(g, 1, 8, _SHAPES[0], 4)
        _paint(g, 5, 3, _DISTRACTORS[0], 6)
        return g
    if name == "no_match":
        # query present but no other object with matching signature
        _paint(g, 1, 1, _SHAPES[0], 8)
        _paint(g, 5, 3, _DISTRACTORS[0], 6)
        _paint(g, 5, 9, _DISTRACTORS[1], 7)
        return g
    if name == "multiple_matches":
        # two non-query objects share the query's signature → ambiguous
        _paint(g, 1, 1, _SHAPES[0], 8)
        _paint(g, 1, 8, _SHAPES[0], 4)
        _paint(g, 5, 3, _SHAPES[0], 6)   # also matches!
        return g
    return g
