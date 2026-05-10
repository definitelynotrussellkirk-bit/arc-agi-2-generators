"""Generator for arc_additional_puzzles_21_set15_bundle:E103 — Bbox crop of color-at-(0,0) (excluding (0,0) itself).

Rule: target color is g[0][0]; collect all cells of that color except
(0,0); subgrid bbox of those cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_distractors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_target_cells, marker_only_at_origin.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "27387ebf1485"
VERSION = "1.1.0"
TASK_ID = "27387ebf1485"
SUMMARY = "Marker color at (0,0); a small shape of the same color elsewhere; distractor blobs of other colors."

INVARIANTS = [
    "(0,0) holds a unique non-bg marker color",
    ">=1 cell of that color elsewhere (forms a shape)",
    "1-2 distractor blobs of different colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_target_cells", "marker_only_at_origin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distractors":  {"type": "int", "default": "2", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "marker_at_origin",
                       "valid": "marker_at_origin"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    marker, c2, c3 = pal
    g[0][0] = marker
    shape = rng.choice([
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
    ])
    top = rng.randint(2, h - 4); left = rng.randint(1, w - 4)
    paint_at(g, top, left, shape, marker)
    sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
    paint_at(g, 1, w - 3, sq, c2)
    g[h - 2][2] = c3; g[h - 2][3] = c3; g[h - 2][4] = c3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # (0,0) is bg → no target color, rule has no anchor
        for r, c in [(2, 3), (3, 3), (3, 4)]:
            g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 6)]:
            g[r][c] = 6
        return g
    if name == "no_target_cells":
        # marker at (0,0) but no other cells of that color → rule's bbox over empty set is undefined
        g[0][0] = 5
        for r, c in [(3, 3), (4, 3), (4, 4)]:
            g[r][c] = 6
        for r, c in [(6, 7), (7, 7)]:
            g[r][c] = 4
        return g
    if name == "marker_only_at_origin":
        # only the (0,0) marker exists with that color, no other instances anywhere → empty target set
        g[0][0] = 5
        return g
    return g
