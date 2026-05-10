"""Generator for arc_additional_puzzles_21_set4:H23.

Rule: sort 1-blobs by (bbox-area desc, r1, c1); recolor by rank starting
at 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_areas, single_frame, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d4171e13daca"
VERSION = "1.1.0"
TASK_ID = "d4171e13daca"
SUMMARY = "Several nested 1-frames of distinct bbox area."

INVARIANTS = [
    "between 2 and 4 nested 1-frames",
    "all bboxes have distinct areas",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_areas", "single_frame", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "concentric_nested",
                       "valid": "concentric_nested"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "frames", "valid": "frames"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 13)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    g = full_grid(h, w, 0)
    r1 = 0; c1 = 0; r2 = h - 1; c2 = w - 1
    for i in range(n_frames):
        if r2 - r1 < 1 or c2 - c1 < 1: break
        for c in range(c1, c2 + 1):
            g[r1][c] = 1; g[r2][c] = 1
        for r in range(r1, r2 + 1):
            g[r][c1] = 1; g[r][c2] = 1
        if r2 - r1 < 4 or c2 - c1 < 4: break
        r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "tied_areas":
        # two frames same bbox area → rank tie, recolor mapping ambiguous
        for c in range(0, 5):
            g[0][c] = 1; g[4][c] = 1
        for r in range(0, 5):
            g[r][0] = 1; g[r][4] = 1
        for c in range(6, 11):
            g[0][c] = 1; g[4][c] = 1
        for r in range(0, 5):
            g[r][6] = 1; g[r][10] = 1
        return g
    if name == "single_frame":
        # one frame → trivial rank, no comparison
        for c in range(0, 5):
            g[0][c] = 1; g[4][c] = 1
        for r in range(0, 5):
            g[r][0] = 1; g[r][4] = 1
        return g
    if name == "no_frames":
        # empty grid → no 1-blobs to recolor
        return g
    return g
