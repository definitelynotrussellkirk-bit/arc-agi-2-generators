"""Generator for arc_puzzle_bank_21_set13_s:S13_M1.

Rule: a blue-count header chooses the area rank of the body object to crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, tied_areas, more_markers_than_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "963dad37593d"
VERSION = "1.1.0"
TASK_ID = "963dad37593d"
SUMMARY = "A blue-count header chooses the area rank of the body object to crop."

INVARIANTS = [
    "background is 0",
    "the top row contains one to three blue cells encoding rank",
    "body objects have distinct areas",
    "the selected object is fully separated from other body objects",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "tied_areas", "more_markers_than_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

RECT_2X3 = [(r, c) for r in range(2) for c in range(3)]
PLUS_5 = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
L_3 = [(0, 0), (1, 0), (1, 1)]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "header_top_objects_below",
                       "valid": "header_top_objects_below"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
        rank = ctx.draw_int("rank", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 14, 15)
        rank = ctx.draw_int("rank", 2, 3)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
        rank = ctx.draw_int("rank", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    for c in range(rank):
        g[0][c] = 1

    r0 = rng.randint(2, 3)
    c0 = rng.randint(1, 2)
    paint_at(g, r0, c0, RECT_2X3, 2)
    paint_at(g, r0, c0 + 6, PLUS_5, 3)
    paint_at(g, h - 3, w - 4, L_3, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # no blue marker → rank undefined, rule has no selector
        paint_at(g, 2, 1, RECT_2X3, 2)
        paint_at(g, 2, 7, PLUS_5, 3)
        paint_at(g, h - 3, w - 4, L_3, 4)
        return g
    if name == "tied_areas":
        # two body objects same area → rank tie, ambiguous which to crop
        g[0][0] = 1
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 2, 7, [(0, 0), (0, 1), (1, 0)], 3)
        paint_at(g, h - 3, w - 4, L_3, 4)
        return g
    if name == "more_markers_than_objects":
        # 4 markers but only 3 body objects → rank exceeds available
        for c in range(4): g[0][c] = 1
        paint_at(g, 2, 1, RECT_2X3, 2)
        paint_at(g, 2, 7, PLUS_5, 3)
        paint_at(g, h - 3, w - 4, L_3, 4)
        return g
    return g
