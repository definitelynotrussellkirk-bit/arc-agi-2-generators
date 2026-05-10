"""Generator for arc_puzzle_bank_21_set12_s:S12_E4 — marker selects smallest neighbor.

Rule: a color-1 marker touches multiple shapes; the smallest adjacent
shape is cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, small_side,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_neighbors, tied_neighbors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "23a0c42b8a1c"
VERSION = "1.1.0"
TASK_ID = "23a0c42b8a1c"
SUMMARY = "A color-1 marker touches multiple shapes; the smallest adjacent shape is cropped."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-1 marker component",
    "the marker touches at least two components of different sizes",
    "the smallest marker neighbor is unique",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_neighbors", "tied_neighbors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..15"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "small_side":     {"type": "str", "default": "rng right|left", "valid": "right|left"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "marker_with_neighbors",
                       "valid": "marker_with_neighbors"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    side = ctx.draw_choice("small_side", ["right", "left"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 4)
    c = rng.randint(3, w - 7)
    g[r][c] = 1
    if side == "right":
        g[r][c + 1] = 3
        _paint(g, [(r + 1, c), (r + 2, c), (r + 2, c + 1)], 4)
    else:
        g[r][c - 1] = 3
        _paint(g, [(r + 1, c), (r + 2, c), (r + 2, c + 1)], 4)
    _paint(g, [(h - 2, w - 3), (h - 2, w - 2)], 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # no color-1 component → no marker to anchor selection
        _paint(g, [(2, 2), (2, 3)], 3)
        _paint(g, [(5, 5), (6, 5)], 4)
        return g
    if name == "no_neighbors":
        # marker exists but is isolated → no neighbor to crop
        g[3][3] = 1
        _paint(g, [(7, 8), (7, 9)], 6)
        return g
    if name == "tied_neighbors":
        # two equally-small marker neighbors → ambiguous "smallest"
        g[3][3] = 1
        g[3][4] = 4
        g[4][3] = 6
        return g
    return g
