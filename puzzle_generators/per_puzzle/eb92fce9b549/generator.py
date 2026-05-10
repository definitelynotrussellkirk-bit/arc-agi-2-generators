"""Generator for arc_additional_puzzles_21_set21_bundle:H143 — Recolor objects by bbox-area rank.

Rule: sort objects by bbox-area desc; first becomes 2, second becomes 3, ...

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_frame, tied_areas, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "eb92fce9b549"
VERSION = "1.1.0"
TASK_ID = "eb92fce9b549"
SUMMARY = "Several nested 1-frames of distinct bbox-area; output recolors by rank starting at 2."

INVARIANTS = [
    "between 2 and 4 nested frames",
    "all bboxes have distinct areas (so rank is unambiguous)",
    "all frames colored 1",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_frame", "tied_areas", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..4",  "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "nested_rectangular_frames",
                       "valid": "nested_rectangular_frames"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 11, 15)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    r1 = 1; c1 = 1
    r2 = h - 2; c2 = w - 2
    for i in range(n_frames):
        if r2 - r1 < 1 or c2 - c1 < 1:
            break
        if r1 == r2 and c1 == c2:
            g[r1][c1] = 1
            break
        for c in range(c1, c2 + 1):
            g[r1][c] = 1
            g[r2][c] = 1
        for r in range(r1, r2 + 1):
            g[r][c1] = 1
            g[r][c2] = 1
        if r2 - r1 < 4 or c2 - c1 < 4:
            break
        r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "single_frame":
        # only one frame → rank=1, output is trivially {2: outer_frame}
        for c in range(1, w - 1):
            g[1][c] = 1; g[h - 2][c] = 1
        for r in range(1, h - 1):
            g[r][1] = 1; g[r][w - 2] = 1
        return g
    if name == "tied_areas":
        # two side-by-side frames with equal bbox area → rank tied, ambiguous mapping
        # left 4x4 frame
        for c in range(1, 5):
            g[1][c] = 1; g[4][c] = 1
        for r in range(1, 5):
            g[r][1] = 1; g[r][4] = 1
        # right 4x4 frame, same area
        for c in range(7, 11):
            g[1][c] = 1; g[4][c] = 1
        for r in range(1, 5):
            g[r][7] = 1; g[r][10] = 1
        return g
    if name == "no_frames":
        # blank → no objects, nothing to rank
        return g
    return g
