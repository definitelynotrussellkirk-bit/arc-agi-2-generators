"""Generator for 37d3e8b2.

Rule: each 8-blob has N internal hole regions; recolor by hole count.

Combinatorial axes (8): grid_h/w, frame1_h, frame1_w, frame2_h, frame2_w,
position_bias, anchor_corner, asymmetry_force.
Degenerates: solid_block, no_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "9d52c9d09009"
VERSION = "1.1.0"
TASK_ID = "9d52c9d09009"
SUMMARY = "1-2 hollow 8-frames with single or double interior holes."

INVARIANTS = [
    ">=1 hollow 8-frame with 1 hole interior",
    ">=1 hollow 8-frame with 2 separate hole regions (split by interior 8 wall)",
]

POSITION_BIASES = ("scattered", "row_aligned", "spread", "rng")
DEGENERATE_TEXTURES = ("solid_block", "no_holes", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "frame1_h":       {"type": "int", "default": "rng 3..h-2", "valid": "3..6"},
    "frame1_w":       {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "frame2_h":       {"type": "int", "default": "rng 3..h-2", "valid": "3..6"},
    "frame2_w":       {"type": "int", "default": "rng 5..7", "valid": "5..9"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 5, 6, 12, 14
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 17, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 8, 14, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    fr1 = int(overrides.get("frame1_h",
                            rng.randint(3, max(3, h - 2))))
    fc1 = int(overrides.get("frame1_w",
                            rng.randint(4, 6)))
    fr1 = max(3, min(fr1, h))
    fc1 = max(4, min(fc1, max(4, w // 2 - 1)))
    r0_1 = rng.randint(0, max(0, h - fr1))
    c0_1 = rng.randint(0, max(0, w // 2 - fc1 - 1))
    draw_rect_outline(g, r0_1, c0_1, fr1, fc1, 8)
    fr2 = int(overrides.get("frame2_h",
                            rng.randint(3, max(3, h - 2))))
    fc2 = int(overrides.get("frame2_w",
                            rng.randint(5, 7)))
    fr2 = max(3, min(fr2, h))
    fc2 = max(5, min(fc2, w - w // 2))
    r0_2 = rng.randint(0, max(0, h - fr2))
    c0_2 = rng.randint(w // 2 + 1, max(w // 2 + 1, w - fc2))
    draw_rect_outline(g, r0_2, c0_2, fr2, fc2, 8)
    mid_c = c0_2 + fc2 // 2
    for r in range(r0_2 + 1, r0_2 + fr2 - 1):
        g[r][mid_c] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 15
    g = full_grid(h, w, 0)
    if name == "solid_block":
        for r in range(2, 5):
            for c in range(2, 6):
                g[r][c] = 8
        return g
    if name == "no_holes":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
