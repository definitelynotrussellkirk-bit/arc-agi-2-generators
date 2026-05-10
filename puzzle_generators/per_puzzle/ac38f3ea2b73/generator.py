"""Generator for arc_puzzle_bank_tenth21:M67.

Rule: a small 7-frame interior is transplanted into a larger 7-frame
(centered).

Combinatorial axes (8): grid_h, grid_w, palette_kind, small_h, small_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_small_frame, no_large_frame, no_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "ac38f3ea2b73"
VERSION = "1.1.0"
TASK_ID = "ac38f3ea2b73"
SUMMARY = "A small 7-frame interior is transplanted into a larger 7-frame."

INVARIANTS = [
    "there are exactly two color-7 rectangular frames",
    "the smaller frame has a nonzero interior pattern",
    "the larger frame interior can contain the smaller frame interior centered",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_small_frame", "no_large_frame", "no_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "20", "valid": "20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "small_h":        {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "small_w":        {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "two_frames",
                       "valid": "two_frames"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        sh = ctx.draw_int("small_h", 5, 5)
        sw = ctx.draw_int("small_w", 5, 5)
    elif difficulty == "hard":
        sh = ctx.draw_int("small_h", 6, 6)
        sw = ctx.draw_int("small_w", 6, 6)
    else:
        sh = ctx.draw_int("small_h", 5, 6)
        sw = ctx.draw_int("small_w", 5, 6)
    g = full_grid(16, 20, 0)
    draw_frame(g, 1, 1, sh, sw, 7)
    draw_frame(g, 3, 10, 13, 18, 7)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 8, 9], 3)
    marks = [(1, 1, colors[0]), (2, 1, colors[0]), (2, 2, colors[1]),
             (sh - 2, sw - 2, colors[2])]
    for r, c, v in marks:
        if r < sh - 1 and c < sw - 1:
            g[1 + r][1 + c] = v
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 20, 0)
    if name == "no_small_frame":
        # only the large frame → no source pattern to transplant
        draw_frame(g, 3, 10, 13, 18, 7)
        return g
    if name == "no_large_frame":
        # only small frame with interior → no destination
        draw_frame(g, 1, 1, 5, 5, 7)
        g[2][2] = 4; g[3][2] = 6
        return g
    if name == "no_interior":
        # both frames present but small frame is empty → nothing to transplant
        draw_frame(g, 1, 1, 5, 5, 7)
        draw_frame(g, 3, 10, 13, 18, 7)
        return g
    return g
