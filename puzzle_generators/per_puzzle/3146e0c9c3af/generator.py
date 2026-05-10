"""Generator for arc_additional_puzzles_21_set3:H16.

Rule: nested 1-frames; for each 0-cell, count enclosing frames; if > 0,
recolor to (depth + 1).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, single_frame, frames_at_edges.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3146e0c9c3af"
VERSION = "1.1.0"
TASK_ID = "3146e0c9c3af"
SUMMARY = "Several nested 1-frames forming concentric structure."

INVARIANTS = [
    "between 3 and 4 nested 1-frames (h≥3, w≥3 each)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "frames_at_edges")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "nested_centered",
                       "valid": "nested_centered"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
        n_frames = ctx.draw_int("n_frames", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_frames = ctx.draw_int("n_frames", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    g = full_grid(h, w, 0)
    r1 = 1; c1 = 1; r2 = h - 2; c2 = w - 2
    for i in range(n_frames):
        if r2 - r1 < 2 or c2 - c1 < 2: break
        for c in range(c1, c2 + 1):
            g[r1][c] = 1; g[r2][c] = 1
        for r in range(r1, r2 + 1):
            g[r][c1] = 1; g[r][c2] = 1
        if r2 - r1 < 4 or c2 - c1 < 4: break
        r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # empty grid → no enclosing structure, depth 0 everywhere
        return g
    if name == "single_frame":
        # one frame → max depth 1, no nesting structure
        for c in range(2, 8): g[2][c] = 1; g[7][c] = 1
        for r in range(2, 8): g[r][2] = 1; g[r][7] = 1
        return g
    if name == "frames_at_edges":
        # outermost frame on edge cells → invariant says interior placement, edge case
        for c in range(0, w): g[0][c] = 1; g[h - 1][c] = 1
        for r in range(0, h): g[r][0] = 1; g[r][w - 1] = 1
        return g
    return g
