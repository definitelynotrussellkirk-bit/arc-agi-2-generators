"""Generator for arc_puzzle_bank_21_set4_d:medium_d06.

A singleton marker shares its color with one larger object. The rule crops that
larger object and centers it on a blank canvas of the original size.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_match_object, multiple_match_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d1f49881a17d"
VERSION = "1.1.0"
TASK_ID = "d1f49881a17d"
SUMMARY = "A singleton color marker selects the larger object of the same color for centering."

INVARIANTS = [
    "exactly one color has both a singleton marker and a larger object",
    "the selected larger object is not already centered",
    "distractor objects, if present, use different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_match_object", "multiple_match_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "marker_plus_match_plus_distractor",
                       "valid": "marker_plus_match_plus_distractor"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
    cells = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    g = full_grid(h, w, 0)
    g[1][w - 2] = color
    _paint(g, h - 5, 1, cells, color)
    g[2][2] = 5
    g[2][3] = 5
    g[3][2] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # larger object exists but no singleton marker → no selection signal
        _paint(g, h - 5, 1, _SHAPES[0], 4)
        g[2][2] = 5; g[2][3] = 5; g[3][2] = 5
        return g
    if name == "no_match_object":
        # marker exists but no larger object of same color → "select match" fails
        g[1][w - 2] = 4
        g[2][2] = 5; g[2][3] = 5; g[3][2] = 5  # only distractor of color 5
        return g
    if name == "multiple_match_objects":
        # 2 larger objects share marker color → ambiguous selection
        g[1][w - 2] = 4
        _paint(g, h - 5, 1, _SHAPES[0], 4)
        _paint(g, 5, 6, _SHAPES[1], 4)  # also same color
        return g
    return g
