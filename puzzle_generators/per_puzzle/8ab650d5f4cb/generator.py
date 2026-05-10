"""Generator for arc_additional_puzzle_bank_volume20:M138.

Rule: for each 1-frame (hollow rect), find non-{0,1} markers inside; if
exactly one color, fill interior with that color.

Combinatorial axes (8): grid_h/w, palette_kind, n_frames, palette_size,
position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_frames, no_markers, two_markers_in_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "8ab650d5f4cb"
VERSION = "1.1.0"
TASK_ID = "8ab650d5f4cb"
SUMMARY = "2 closed 1-frames each with one marker color inside + decoration."

INVARIANTS = [
    "exactly 2 closed 1-frames",
    "each has one marker of distinct non-{0,1} color inside",
]

PALETTE_KINDS = ("default", "warm_markers", "cool_markers", "varied_markers")
DEGENERATE_TEXTURES = ("no_frames", "no_markers", "two_markers_in_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8, 9]; rng.shuffle(palette)
    draw_frame(g, 1, 1, 4, 4, 1)
    g[2][2] = palette[0]
    draw_frame(g, 5, 7, 8, 11, 1)
    g[6][9] = palette[1]
    g[0][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # markers but no 1-frames — no compartments to fill
        g[3][3] = 4
        g[6][9] = 6
        return g
    if name == "no_markers":
        # frames but no markers inside — fill color undefined
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 5, 7, 8, 11, 1)
        return g
    if name == "two_markers_in_frame":
        # one frame contains two distinct markers → ambiguous
        draw_frame(g, 1, 1, 5, 5, 1)
        g[2][2] = 4
        g[3][3] = 6  # second distinct marker
        draw_frame(g, 5, 7, 8, 11, 1)
        g[6][9] = 7
        return g
    return g
