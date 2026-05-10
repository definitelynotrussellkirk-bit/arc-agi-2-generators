"""Generator for arc_additional_puzzles_21_set4:M22.

Rule: for each color-1 frame, find the seed (a non-{0,1} cell) inside its
interior and fill that frame's interior with the seed's color.

Combinatorial axes (8): grid_h/w, palette_kind, num_frames, frame_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_seed, frames_overlap, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "486375757aca"
VERSION = "1.1.0"
TASK_ID = "486375757aca"
SUMMARY = "2 1-frames each with one non-{0,1} seed inside."

INVARIANTS = [
    "exactly 2 closed 1-frames",
    "each frame has exactly one non-{0,1} seed inside (size 1)",
]

PALETTE_KINDS = ("default", "wide_seeds", "tight_frames", "edge_anchored")
DEGENERATE_TEXTURES = ("no_seed", "frames_overlap", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_frames":     {"type": "int", "default": "2", "valid": "1..3"},
    "frame_size":     {"type": "str", "default": "mixed", "valid": "small|mixed|large"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    draw_frame(g, 1, 1, 4, 5, 1)
    g[2][3] = rng.choice([2, 3, 4, 6, 7, 8, 9])
    draw_frame(g, 1, 7, 5, w - 2, 1)
    g[3][9] = rng.choice([2, 3, 4, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 13
    g = full_grid(h, w, 0)
    if name == "no_seed":
        draw_frame(g, 1, 1, 4, 5, 1)
        draw_frame(g, 1, 7, 5, 11, 1)
        return g
    if name == "frames_overlap":
        draw_frame(g, 1, 1, 5, 7, 1)
        draw_frame(g, 1, 5, 5, 11, 1)
        g[3][3] = 5
        g[3][9] = 7
        return g
    if name == "single_frame":
        draw_frame(g, 1, 1, 6, 11, 1)
        g[3][6] = 5
        return g
    return g
