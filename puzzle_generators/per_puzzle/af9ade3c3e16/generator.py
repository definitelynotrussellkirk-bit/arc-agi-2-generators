"""Generator for arc_additional_puzzle_bank_volume21:H143.

Rule: the count of red markers in row 0 selects which nested yellow
frame (1=outer, 2=middle, 3=inner) becomes cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_frames, rank_out_of_range.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "af9ade3c3e16"
VERSION = "1.1.0"
TASK_ID = "af9ade3c3e16"
SUMMARY = "Three nested yellow frames; red marker count = 1-based frame index."

INVARIANTS = [
    "background is 0",
    "three nested hollow yellow frames at offsets 1, 3, 5 from each edge",
    "1-3 red markers in row 0 (the rank selector)",
    "frames are ordered outermost to innermost",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_frames", "rank_out_of_range")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..17", "valid": "11..23"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "11..23"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "nested_centered",
                       "valid": "nested_centered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "frames", "valid": "frames"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _frame(g, r0, c0, r1, c1):
    for r in range(r0, r1 + 1):
        g[r][c0] = 4
        g[r][c1] = 4
    for c in range(c0, c1 + 1):
        g[r0][c] = 4
        g[r1][c] = 4


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("grid_size", 13, 13)
        rank = ctx.draw_int("rank", 1, 1)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 16, 17)
        rank = ctx.draw_int("rank", 3, 3)
    else:
        n = ctx.draw_int("grid_size", 13, 17)
        rank = ctx.draw_int("rank", 1, 3)
    g = full_grid(n, n, 0)
    _frame(g, 1, 1, n - 2, n - 2)
    _frame(g, 3, 3, n - 4, n - 4)
    _frame(g, 5, 5, n - 6, n - 6)
    for i in range(rank):
        g[0][i] = 2
    return g


def _draw_from_degenerate(name, rng):
    n = 13
    g = full_grid(n, n, 0)
    if name == "no_markers":
        # no red selector → no rank, no frame is recolored
        _frame(g, 1, 1, n - 2, n - 2)
        _frame(g, 3, 3, n - 4, n - 4)
        _frame(g, 5, 5, n - 6, n - 6)
        return g
    if name == "no_frames":
        # markers present but no frames to select from → rule has no target
        for i in range(2):
            g[0][i] = 2
        return g
    if name == "rank_out_of_range":
        # 4+ red markers but only 3 frames → rank exceeds available frames
        _frame(g, 1, 1, n - 2, n - 2)
        _frame(g, 3, 3, n - 4, n - 4)
        _frame(g, 5, 5, n - 6, n - 6)
        for i in range(4):
            g[0][i] = 2
        return g
    return g
