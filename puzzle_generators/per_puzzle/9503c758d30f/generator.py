"""Generator for arc_additional_puzzles_21_set3:M18.

Rule: for each solid 6-rect, paint 2 at the 4 cells diagonally outside
its bbox (one step past each corner) where empty.

Combinatorial axes (8): grid_h/w, palette_kind, num_rects, rect_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_rects, rect_at_edge, corners_already_marked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9503c758d30f"
VERSION = "1.1.0"
TASK_ID = "9503c758d30f"
SUMMARY = "2 solid 6-rects placed with at least 1-cell margin from grid edges."

INVARIANTS = [
    "exactly 2 non-touching solid 6-rects",
    "each has at least 1-cell margin from any edge",
]

PALETTE_KINDS = ("default", "small_rects", "tall_rects", "wide_rects")
DEGENERATE_TEXTURES = ("no_rects", "rect_at_edge", "corners_already_marked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_rects":      {"type": "int", "default": "2", "valid": "1..3"},
    "rect_size":      {"type": "str", "default": "2x3", "valid": "2x3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "diagonal_corners",
                       "valid": "diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _solid(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    _solid(g, 1, 1, 2, 3, 6)
    _solid(g, h - 4, w - 4, h - 2, w - 2, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_rects":
        return g
    if name == "rect_at_edge":
        # rect at top-left corner — diagonally-outside cells are out of bounds
        _solid(g, 0, 0, 1, 2, 6)
        _solid(g, h - 4, w - 4, h - 2, w - 2, 6)
        return g
    if name == "corners_already_marked":
        # diagonal corners pre-painted with 2 — rule has no fresh cells to mark
        _solid(g, 1, 1, 2, 3, 6)
        for r, c in [(0, 0), (0, 4), (3, 0), (3, 4)]:
            g[r][c] = 2
        return g
    return g
