"""Generator for arc_puzzle_bank_21_set6_s:S6_H1 — fill rooms by inner seed color.

Rule: a hollow color-8 frame with interior 8-walls subdividing it into rooms.
Each room may have a single colored seed; output fills the room with that seed's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seeds, no_inner_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5271d2407456"
VERSION = "1.1.0"
TASK_ID = "5271d2407456"

SUMMARY = "Color-8 outer frame + interior 8-walls + 1-3 colored seeds in distinct non-{0, 8} colors."

INVARIANTS = [
    "background is 0",
    "exactly one hollow color-8 outer frame",
    "1-2 interior 8-walls (full row/col of frame interior) divide the interior",
    "1-3 colored seeds in distinct non-{0, 8} colors inside the frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seeds", "no_inner_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "8frame_with_inner_walls_and_seeds",
                       "valid": "8frame_with_inner_walls_and_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
        n_seeds = ctx.draw_int("n_seeds", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        n_seeds = ctx.draw_int("n_seeds", 1, 3)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    # outer frame
    fr0 = 1; fc0 = 1; fr1 = h - 2; fc1 = w - 2
    draw_frame(g, fr0, fc0, fr1, fc1, 8)
    # interior wall (one row, full width)
    iw_r = (fr0 + fr1) // 2
    for c in range(fc0, fc1 + 1): g[iw_r][c] = 8
    # seeds in interior cells (not on walls)
    seed_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n_seeds)
    for color in seed_colors:
        for _t in range(60):
            r = rng.randint(fr0 + 1, fr1 - 1); c = rng.randint(fc0 + 1, fc1 - 1)
            if g[r][c] != 0: continue
            g[r][c] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # seeds but no 8-frame → no rooms defined
        g[2][3] = 4; g[5][7] = 6
        return g
    if name == "no_seeds":
        # frame + walls but no seeds → no fill colors defined for any room
        draw_frame(g, 1, 1, h - 2, w - 2, 8)
        for c in range(1, w - 1): g[(h - 1) // 2][c] = 8
        return g
    if name == "no_inner_wall":
        # frame + seeds but no interior wall → only one room, all seeds compete
        draw_frame(g, 1, 1, h - 2, w - 2, 8)
        g[2][3] = 4; g[5][7] = 6
        return g
    return g
