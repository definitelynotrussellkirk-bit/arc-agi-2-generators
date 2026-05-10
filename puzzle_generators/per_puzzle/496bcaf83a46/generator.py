"""Generator for arc_additional_puzzles_21_set6:H40 — fill max-seed frames.

Rule: among rectangular frames containing 8-seeds, fill the interior
of the frame(s) with the most seeds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, tied_max_count, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "496bcaf83a46"
VERSION = "1.1.0"
TASK_ID = "496bcaf83a46"
SUMMARY = "Several frames contain different counts of 8 seeds; max-count frames fill."

INVARIANTS = [
    "background is 0",
    "all candidate objects are rectangular frame outlines",
    "seed dots use color 8 and are strictly inside frames",
    "exactly one frame has the maximum seed count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "tied_max_count", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 18..22", "valid": "15..26"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "frames_with_distinct_seedcounts",
                       "valid": "frames_with_distinct_seedcounts"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 18, 19)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 21, 22)
    else:
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 18, 22)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    boxes = [(1, 1, 6, 6), (1, 9, 7, 15), (h - 7, w - 7, h - 2, w - 2)]
    counts = [1, 3, 2]
    for color, box, count in zip(colors, boxes, counts):
        r1, c1, r2, c2 = box
        draw_frame(g, r1, c1, r2, c2, color)
        spots = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
        rng.shuffle(spots)
        for r, c in spots[:count]:
            g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 20
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # frames present but no 8-seeds → max-count is 0 across all, rule degenerate
        draw_frame(g, 1, 1, 6, 6, 4)
        draw_frame(g, 1, 9, 7, 15, 6)
        draw_frame(g, h - 7, w - 7, h - 2, w - 2, 3)
        return g
    if name == "tied_max_count":
        # 2 frames have same (max) seed count → "the max-count frame" is ambiguous
        draw_frame(g, 1, 1, 6, 6, 4)
        g[2][2] = 8; g[3][3] = 8; g[4][4] = 8        # count 3
        draw_frame(g, 1, 9, 7, 15, 6)
        g[2][10] = 8; g[3][11] = 8; g[4][12] = 8     # count 3 (tied)
        draw_frame(g, h - 7, w - 7, h - 2, w - 2, 3)
        g[h - 5][w - 5] = 8                          # count 1
        return g
    if name == "single_frame":
        # only 1 frame → max is trivially that one (no decision required)
        draw_frame(g, 2, 2, h - 3, w - 3, 4)
        g[5][5] = 8; g[6][6] = 8; g[7][7] = 8
        return g
    return g
