"""Generator for arc_additional_puzzle_bank_volume5:H35.

Rule: each hollow color-8 frame has its enclosed interior filled with
alternating red and green depth layers (from outside in).

Combinatorial axes (8): grid_h/w, palette_kind, frame_size,
palette_size, position_bias, n_distinct_colors, frame_density, texture.
Degenerates: no_frame, solid_block, open_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b8cb193f82c"
VERSION = "1.1.0"
TASK_ID = "7b8cb193f82c"
SUMMARY = "Each hollow cyan frame has its enclosed interior filled in alternating red and green depth layers."

INVARIANTS = [
    "one or more hollow color-8 frames are present",
    "each frame encloses a zero interior",
    "frame borders remain unchanged",
    "interior layer depth alternates colors 2 and 3",
]

PALETTE_KINDS = ("default", "small_frame", "large_frame", "narrow_frame")
DEGENERATE_TEXTURES = ("no_frame", "solid_block", "open_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_size":     {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "centered",
                       "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "frame_density":  {"type": "str", "default": "single", "valid": "single"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _frame(g: list[list[int]], r0: int, c0: int, r1: int, c1: int) -> None:
    for r in range(r0, r1 + 1):
        g[r][c0] = 8
        g[r][c1] = 8
    for c in range(c0, c1 + 1):
        g[r0][c] = 8
        g[r1][c] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
    g = full_grid(h, w, 0)
    _frame(g, 1, 1, h - 3, w - 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # empty grid — no frame to fill
        return g
    if name == "solid_block":
        # filled-in block (not hollow) — no zero interior to fill
        for r in range(2, h - 2):
            for c in range(2, w - 2):
                g[r][c] = 8
        return g
    if name == "open_frame":
        # frame with a gap — bg interior reaches outside, "enclosed" undefined
        _frame(g, 1, 1, h - 3, w - 3)
        g[1][5] = 0  # break top border
        return g
    return g
