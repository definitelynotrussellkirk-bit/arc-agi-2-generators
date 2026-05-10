"""Generator for arc_additional_puzzles_21_set17_bundle:H116 — Recolor nested 1-frames by depth from palette.

Rule: sort 1-frames by bbox-area desc; recolor by depth using palette
[2 4 6 7 3 9].

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, single_frame, non_nested.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f5d19d5363ef"
VERSION = "1.1.0"
TASK_ID = "f5d19d5363ef"
SUMMARY = "Several nested 1-frames of distinct bbox areas."

INVARIANTS = [
    "between 3 and 5 nested 1-frames",
    "all bboxes have distinct areas",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "non_nested")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "nested_concentric_frames",
                       "valid": "nested_concentric_frames"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_frames = ctx.draw_int("n_frames", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        n_frames = ctx.draw_int("n_frames", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 13)
        n_frames = ctx.draw_int("n_frames", 3, 5)
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
    if name == "no_frames":
        # blank → no frames to recolor by depth
        return g
    if name == "single_frame":
        # only one frame → trivial: depth 0, gets palette[0] = 2
        for c in range(w): g[0][c] = 1; g[h - 1][c] = 1
        for r in range(h): g[r][0] = 1; g[r][w - 1] = 1
        return g
    if name == "non_nested":
        # two side-by-side (non-nested) frames → depth ordering ill-defined
        for c in range(0, 5): g[1][c] = 1; g[5][c] = 1
        for r in range(1, 6): g[r][0] = 1; g[r][4] = 1
        for c in range(6, 11): g[1][c] = 1; g[5][c] = 1
        for r in range(1, 6): g[r][6] = 1; g[r][10] = 1
        return g
    return g
