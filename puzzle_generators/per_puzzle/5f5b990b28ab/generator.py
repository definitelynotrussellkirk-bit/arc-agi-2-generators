"""Generator for arc_additional_puzzles_21_set18_bundle:M125.

Rule: sort 8-frames by bbox area desc; assign palette
[2,4,6,7,3,5,9] by depth.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_areas, single_frame, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5f5b990b28ab"
VERSION = "1.1.0"
TASK_ID = "5f5b990b28ab"
SUMMARY = "Several nested 8-frames of distinct bbox areas."

INVARIANTS = [
    "between 2 and 4 nested 8-frames",
    "all bboxes have distinct areas",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_areas", "single_frame", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 11)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    g = full_grid(h, w, 0)
    r1 = 1; c1 = 1; r2 = h - 2; c2 = w - 2
    for i in range(n_frames):
        if r2 - r1 < 1 or c2 - c1 < 1: break
        for c in range(c1, c2 + 1):
            g[r1][c] = 8; g[r2][c] = 8
        for r in range(r1, r2 + 1):
            g[r][c1] = 8; g[r][c2] = 8
        if r2 - r1 < 4 or c2 - c1 < 4: break
        r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "tied_areas":
        # two 8-frames same bbox area → depth ordering ambiguous
        for c in range(0, 5): g[0][c] = 8; g[4][c] = 8
        for r in range(0, 5): g[r][0] = 8; g[r][4] = 8
        for c in range(7, 12): g[0][c] = 8; g[4][c] = 8
        for r in range(0, 5): g[r][7] = 8; g[r][11] = 8
        return g
    if name == "single_frame":
        # one frame → trivial depth, no comparison
        for c in range(2, 9): g[2][c] = 8; g[8][c] = 8
        for r in range(2, 9): g[r][2] = 8; g[r][8] = 8
        return g
    if name == "no_frames":
        # empty grid → no 8-frames to recolor
        return g
    return g
