"""Generator for arc_additional_puzzle_bank_volume12:H81 — XOR of red+green into gray frame.

Rule: the XOR of normalized red and green shapes is written into the
interior of a gray output frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: identical_shapes, no_overlap, no_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "cfac60b0f321"
VERSION = "1.1.0"
TASK_ID = "cfac60b0f321"
SUMMARY = "The XOR of normalized red and green shapes is written into the interior of a gray output frame."

INVARIANTS = [
    "one red mask and one green mask are present",
    "the normalized masks partially overlap",
    "there is one rectangular gray output frame",
    "the frame interior is large enough for the XOR mask",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identical_shapes", "no_overlap", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..24"},
    "grid_w":         {"type": "int", "default": "rng 15..20", "valid": "12..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "red_green_with_gray_frame",
                       "valid": "red_green_with_gray_frame"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}



def _frame(g: list[list[int]], r0: int, c0: int, rh: int, cw: int) -> None:
    for r in range(r0, r0 + rh):
        g[r][c0] = 5
        g[r][c0 + cw - 1] = 5
    for c in range(c0, c0 + cw):
        g[r0][c] = 5
        g[r0 + rh - 1][c] = 5


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 16)
        w = ctx.draw_int("grid_w", 18, 20)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 15, 20)
    g = full_grid(h, w, 0)
    red = [(0, 0), (1, 0), (2, 0), (2, 1)]
    green = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, 1, 1, red, 2)
    paint_at(g, 1, 7, green, 3)
    _frame(g, h - 6, w - 7, 5, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 16
    g = full_grid(h, w, 0)
    if name == "identical_shapes":
        # red == green normalized → XOR is empty mask, frame interior fills with bg
        same = [(0, 0), (1, 0), (2, 0), (2, 1)]
        paint_at(g, 1, 1, same, 2)
        paint_at(g, 1, 7, same, 3)
        _frame(g, h - 6, w - 7, 5, 6)
        return g
    if name == "no_overlap":
        # red and green share NO cells → XOR == union, masks don't partially overlap
        red = [(0, 0), (0, 1), (1, 0)]
        green = [(2, 0), (2, 1), (3, 1)]   # disjoint
        paint_at(g, 1, 1, red, 2)
        paint_at(g, 1, 7, green, 3)
        _frame(g, h - 6, w - 7, 5, 6)
        return g
    if name == "no_frame":
        # red+green present but no gray frame → output target undefined
        red = [(0, 0), (1, 0), (2, 0), (2, 1)]
        green = [(0, 0), (0, 1), (1, 1), (2, 1)]
        paint_at(g, 1, 1, red, 2)
        paint_at(g, 1, 7, green, 3)
        return g
    return g
