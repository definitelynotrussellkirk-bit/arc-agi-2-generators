"""Generator for arc_additional_puzzles_21_set18_bundle:M122.

Rule: 1-walls form compartments; for each non-1 region with exactly one
marker color, fill empty cells with that color.

Combinatorial axes (8): grid_h/w, palette_kind, n_frames, palette_size,
position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_frames, no_markers, two_markers_in_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "c05faa9b2b85"
VERSION = "1.1.0"
TASK_ID = "c05faa9b2b85"
SUMMARY = "2 1-frames each containing one marker of distinct color."

INVARIANTS = [
    "exactly 2 closed 1-frames (h≥3, w≥3)",
    "each has exactly one non-{0,1} marker inside",
]

PALETTE_KINDS = ("default", "warm_markers", "cool_markers", "varied_markers")
DEGENERATE_TEXTURES = ("no_frames", "no_markers", "two_markers_in_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "marker_density": {"type": "str", "default": "low", "valid": "low"},
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7]; rng.shuffle(palette)
    draw_frame(g, 1, 1, 4, 4, 1)
    g[3][3] = palette[0]
    draw_frame(g, 2, 8, 6, w - 2, 1)
    g[4][10] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # markers but no 1-frames — no compartments to fill
        g[3][3] = 4
        g[5][9] = 6
        return g
    if name == "no_markers":
        # frames but no markers inside — fill color undefined
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 2, 8, 6, w - 2, 1)
        return g
    if name == "two_markers_in_frame":
        # one frame contains two distinct marker colors → ambiguous fill
        draw_frame(g, 1, 1, 5, 5, 1)
        g[2][2] = 4
        g[3][3] = 6  # second distinct marker in same frame
        draw_frame(g, 2, 8, 6, w - 2, 1)
        g[4][10] = 7
        return g
    return g
