"""Generator for arc_additional_puzzle_bank_volume12:M79.

Rule: the gray rectangular frame containing one marker has its
interior filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, all_marked, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5751ed9bdf85"
VERSION = "1.1.0"
TASK_ID = "5751ed9bdf85"
SUMMARY = "The gray rectangular frame containing one marker has its interior filled."

INVARIANTS = [
    "background is 0",
    "gray frame components are hollow rectangles",
    "exactly one frame contains one non-gray marker",
    "unmarked frames remain unchanged",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "all_marked", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "10..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "two_frames", "valid": "two_frames"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 13, 17)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    left_w = rng.randint(4, 5)
    right_w = rng.randint(4, 5)
    r0 = rng.randint(1, h - 7)
    r1 = r0 + rng.randint(4, 5)
    draw_frame(g, r0, 1, r1, left_w, 5)
    draw_frame(g, r0, w - right_w - 1, r1, w - 2, 5)
    marker_color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    g[rng.randint(r0 + 1, r1 - 1)][rng.randint(2, left_w - 1)] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # neither frame has a marker → no frame qualifies for fill
        draw_frame(g, 1, 1, 6, 5, 5)
        draw_frame(g, 1, 8, 6, 12, 5)
        return g
    if name == "all_marked":
        # both frames have markers → "the one with marker" is ambiguous
        draw_frame(g, 1, 1, 6, 5, 5)
        draw_frame(g, 1, 8, 6, 12, 5)
        g[3][3] = 4
        g[3][10] = 7
        return g
    if name == "no_frames":
        # marker exists but no frames → nothing to fill
        g[5][7] = 6
        return g
    return g
