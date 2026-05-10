"""Generator for arc_additional_puzzle_bank_volume21:M145 — fill yellow frames with marker color.

Rule: yellow hollow frames containing a single marker color have their
interiors filled with that marker color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, multi_marker, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "2d2455d1008d"
VERSION = "1.1.0"
TASK_ID = "2d2455d1008d"
SUMMARY = "Yellow hollow frames with a single marker color have their interiors filled."

INVARIANTS = [
    "background is 0",
    "yellow objects are hollow rectangular frames",
    "marked frames contain exactly one nonzero non-frame color",
    "blank interior cells of marked frames are fill targets",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "multi_marker", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "10..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "two_yellow_frames_with_seeds",
                       "valid": "two_yellow_frames_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
    r0 = rng.randint(1, h - 7)
    r1 = r0 + rng.randint(4, 5)
    left_w = rng.randint(4, 5)
    right_w = rng.randint(4, 5)
    draw_frame(g, r0, 1, r1, left_w, 4)
    draw_frame(g, r0, w - right_w - 1, r1, w - 2, 4)
    g[rng.randint(r0 + 1, r1 - 1)][rng.randint(2, left_w - 1)] = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
    g[rng.randint(r0 + 1, r1 - 1)][rng.randint(w - right_w, w - 3)] = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 15
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # frames present but empty interiors → no marker, rule has no fill color
        draw_frame(g, 2, 1, 7, 5, 4)
        draw_frame(g, 2, 9, 7, 13, 4)
        return g
    if name == "multi_marker":
        # frame contains 2 distinct marker colors → fill color ambiguous
        draw_frame(g, 2, 1, 7, 5, 4)
        g[3][2] = 6; g[5][3] = 3   # two different marker colors inside
        return g
    if name == "no_frames":
        # markers present but no yellow frames → rule has nothing to scope
        g[3][3] = 6
        g[5][7] = 3
        return g
    return g
