"""Generator for arc_additional_puzzles_21_set8:H53 — rank+transform a candidate, center in frame.

Rule: rank candidate components by area, transform the requested one,
and center it in a frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rank, no_frame, no_candidates.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "182d3949bec6"
VERSION = "1.1.0"
TASK_ID = "182d3949bec6"
SUMMARY = "Rank candidate components by area, transform the requested one, and center it in a frame."

INVARIANTS = [
    "cell (0,0) gives a one-based area rank",
    "the last cell of row 0 gives the transform command",
    "one color-8 rectangular frame is the destination",
    "candidate components have distinct areas and all transforms fit inside the frame interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rank", "no_frame", "no_candidates")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "transform":      {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "rank_transform_with_frame",
                       "valid": "rank_transform_with_frame"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (2, 2), (3, 1)],
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
        rank = ctx.draw_int("rank", 1, 1)
        transform = ctx.draw_int("transform", 1, 1)
    elif difficulty == "hard":
        rank = ctx.draw_int("rank", 2, 3)
        transform = ctx.draw_int("transform", 2, 4)
    else:
        rank = ctx.draw_int("rank", 1, 3)
        transform = ctx.draw_int("transform", 1, 4)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 9], 3)

    g = full_grid(12, 16, 0)
    g[0][0] = rank
    g[0][15] = transform
    draw_frame(g, 3, 9, 10, 14, 8)
    _paint(g, 2, 1, _SHAPES[0], colors[0])
    _paint(g, 5, 1, _SHAPES[1], colors[1])
    _paint(g, 7, 5, _SHAPES[2], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 16, 0)
    if name == "no_rank":
        # frame + candidates + transform but (0,0) is bg → no rank to apply
        g[0][15] = 2
        draw_frame(g, 3, 9, 10, 14, 8)
        _paint(g, 2, 1, _SHAPES[0], 4)
        _paint(g, 5, 1, _SHAPES[1], 6)
        _paint(g, 7, 5, _SHAPES[2], 7)
        return g
    if name == "no_frame":
        # rank + transform + candidates but no 8-frame → nowhere to center stamp
        g[0][0] = 2
        g[0][15] = 3
        _paint(g, 2, 1, _SHAPES[0], 4)
        _paint(g, 5, 1, _SHAPES[1], 6)
        _paint(g, 7, 5, _SHAPES[2], 7)
        return g
    if name == "no_candidates":
        # rank + transform + frame but no body candidates → no shape to pick
        g[0][0] = 2
        g[0][15] = 3
        draw_frame(g, 3, 9, 10, 14, 8)
        return g
    return g
