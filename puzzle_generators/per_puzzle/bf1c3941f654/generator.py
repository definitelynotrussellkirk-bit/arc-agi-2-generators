"""Generator for arc_additional_puzzles_21_set2:M13 — Recolor 2-cells inside 1-frames to 4.

Rule: for each closed 1-frame, recolor 2-cells strictly inside its
bbox to 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_2_inside, broken_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "bf1c3941f654"
VERSION = "1.1.0"
TASK_ID = "bf1c3941f654"
SUMMARY = "2 closed 1-frames each containing one 2-cell + decoration."

INVARIANTS = [
    "exactly 2 closed 1-frames (h≥3, w≥3)",
    "each contains exactly one 2-cell strictly inside",
    "1-2 2-cells outside frames (decoration that should NOT be recolored)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_2_inside", "broken_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "10..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "13..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_1frames_with_2_seeds",
                       "valid": "two_1frames_with_2_seeds"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    draw_frame(g, 1, 1, 4, 5, 1)
    inside1 = rng.choice([(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4)])
    g[inside1[0]][inside1[1]] = 2
    draw_frame(g, 5, 6, 8, 11, 1)
    inside2 = rng.choice([(6, 7), (6, 8), (6, 9), (6, 10), (7, 7), (7, 9)])
    g[inside2[0]][inside2[1]] = 2
    g[0][w - 1] = 2
    if rng.random() < 0.5:
        g[h - 1][1] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # 2-cells present but no 1-frames → rule has nothing to scope inside
        g[3][5] = 2
        g[7][9] = 2
        return g
    if name == "no_2_inside":
        # frames present but interior empty → no 2-cells to recolor
        draw_frame(g, 1, 1, 4, 5, 1)
        draw_frame(g, 5, 6, 8, 11, 1)
        g[0][w - 1] = 2   # only outside the frames
        return g
    if name == "broken_frame":
        # frame has a missing edge cell → not closed, "interior" undefined
        draw_frame(g, 1, 1, 4, 5, 1)
        g[1][3] = 0   # gap in top edge
        g[2][3] = 2   # 2-cell in supposed interior
        return g
    return g
