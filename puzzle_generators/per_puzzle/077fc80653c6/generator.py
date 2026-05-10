"""Generator for arc_puzzle_bank_21_set13_s:S13_H3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, feature,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_reference, no_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "077fc80653c6"
VERSION = "1.1.0"
TASK_ID = "077fc80653c6"
SUMMARY = "Transfer the red reference object's feature triple to select a matching right-panel candidate."

INVARIANTS = [
    "a full color-5 column splits reference and candidate panels",
    "the left panel contains one red reference component",
    "exactly one right-panel candidate shares the reference area, hole count, and symmetry class",
    "the selected right-panel candidate is cropped and recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_reference", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "feature":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "ref_plus_candidates_5col_split",
                       "valid": "ref_plus_candidates_5col_split"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_FEATURE_SHAPES = [
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]

_DISTRACTORS = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
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
        idx = ctx.draw_int("feature", 0, 2)
    elif difficulty == "hard":
        idx = ctx.draw_int("feature", 3, 5)
    else:
        idx = ctx.draw_int("feature", 0, len(_FEATURE_SHAPES) - 1)
    colors = rng.sample([3, 4, 6, 7, 8, 9], 3)
    g = full_grid(11, 16, 0)
    for r in range(11):
        g[r][7] = 5
    _paint(g, 1, 1, _FEATURE_SHAPES[idx], 2)
    _paint(g, 1, 9, _FEATURE_SHAPES[idx], colors[0])
    _paint(g, 6, 9, _DISTRACTORS[idx], colors[1])
    _paint(g, 6, 13, [(0, 0), (1, 0), (1, 1)], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 16, 0)
    if name == "no_divider":
        # ref + candidates but no 5-col splitting them
        _paint(g, 1, 1, _FEATURE_SHAPES[0], 2)
        _paint(g, 1, 9, _FEATURE_SHAPES[0], 4)
        _paint(g, 6, 9, _DISTRACTORS[0], 6)
        return g
    if name == "no_reference":
        # divider + candidates but no red reference
        for r in range(11): g[r][7] = 5
        _paint(g, 1, 9, _FEATURE_SHAPES[0], 4)
        _paint(g, 6, 9, _DISTRACTORS[0], 6)
        return g
    if name == "no_match":
        # ref + candidates but no candidate matches reference shape
        for r in range(11): g[r][7] = 5
        _paint(g, 1, 1, _FEATURE_SHAPES[0], 2)
        _paint(g, 1, 9, _DISTRACTORS[0], 4)
        _paint(g, 6, 9, _DISTRACTORS[1], 6)
        return g
    return g
