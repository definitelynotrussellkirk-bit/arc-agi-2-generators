"""Generator for arc_puzzle_bank_21_set3:S3_H4.

A color-4 frame defines a vertical mirror axis. Interior colored cells are
placed on the left half and mirrored by the rule into the right half.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, even_width_frame, no_left_content.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9126300ec565"
VERSION = "1.1.0"
TASK_ID = "9126300ec565"
SUMMARY = "Mirror colored interior cells across a vertical axis inside a frame."

INVARIANTS = [
    "color 4 is a rectangular frame",
    "the frame interior has odd width and a vertical center axis",
    "non-frame colored cells inside the frame are mirrored horizontally",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "even_width_frame", "no_left_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_h":        {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "frame_w":        {"type": "int", "default": "rng 9..11 odd", "valid": "7..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks":        {"type": "int", "default": "4", "valid": "2..7"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "frame_with_left_content",
                       "valid": "frame_with_left_content"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_frame(g, top, left, bottom, right):
    for c in range(left, right + 1):
        g[top][c] = 4
        g[bottom][c] = 4
    for r in range(top, bottom + 1):
        g[r][left] = 4
        g[r][right] = 4


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        fh = ctx.draw_int("frame_h", 6, 6)
        fw = ctx.draw_choice("frame_w", [9])
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 7, 8)
        fw = ctx.draw_choice("frame_w", [11])
    else:
        fh = ctx.draw_int("frame_h", 6, 8)
        fw = ctx.draw_choice("frame_w", [9, 11])
    h = fh + 4
    w = fw + 4
    g = full_grid(h, w, 0)
    top, left = 2, 2
    bottom, right = top + fh - 1, left + fw - 1
    _draw_frame(g, top, left, bottom, right)
    center = (left + right) // 2
    colors = rng.sample([2, 3, 5, 6, 7, 8, 9], 4)
    for color in colors:
        r = rng.randint(top + 1, bottom - 1)
        c = rng.randint(left + 1, center)
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # colored interior cells without 4-frame → no mirror axis
        g[3][3] = 5
        g[5][4] = 6
        g[7][3] = 7
        return g
    if name == "even_width_frame":
        # frame with even interior width → no integer center axis
        _draw_frame(g, 2, 2, 9, 11)  # interior width 8 (even)
        g[4][3] = 5
        g[6][4] = 6
        return g
    if name == "no_left_content":
        # frame present but no left-half content → nothing to mirror
        _draw_frame(g, 2, 2, 9, 12)
        return g
    return g
