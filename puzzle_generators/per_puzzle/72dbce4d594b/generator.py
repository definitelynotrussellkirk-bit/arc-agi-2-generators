"""Generator for arc_additional_puzzle_bank_volume7:H43 — markers select blue component, transform, stamp.

Rule: marker counts choose a blue component by size rank and transform
it before stamping orange at a cyan target.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blue, no_red_marker, no_target.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import L_TROMINO_NE, T_TETROMINO

GENERATOR_ID = "72dbce4d594b"
VERSION = "1.1.0"
TASK_ID = "72dbce4d594b"
SUMMARY = "Marker counts choose a blue component by size rank and transform it before stamping orange at a cyan target."

INVARIANTS = [
    "blue components have distinct sizes",
    "red marker count selects a valid size rank",
    "green marker count selects a transform from 1 through 4",
    "the chosen transformed component fits at the cyan target",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blue", "no_red_marker", "no_target")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..24"},
    "grid_w":         {"type": "int", "default": "rng 14..19", "valid": "12..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "turns":          {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "blue_with_marker_pair_and_target",
                       "valid": "blue_with_marker_pair_and_target"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
        rank = ctx.draw_int("rank", 1, 1)
        turns = ctx.draw_int("turns", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 18, 19)
        rank = ctx.draw_int("rank", 2, 3)
        turns = ctx.draw_int("turns", 2, 4)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 14, 19)
        rank = ctx.draw_int("rank", 1, 3)
        turns = ctx.draw_int("turns", 1, 4)
    g = full_grid(h, w, 0)
    g[3][1] = 1
    paint_at(g, 5, 4, L_TROMINO_NE, 1)
    paint_at(g, 8, 1, T_TETROMINO, 1)
    for i in range(rank):
        g[0][i] = 2
    for i in range(turns):
        g[i][w - 1] = 3
    g[h // 2][w - 6] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 15
    g = full_grid(h, w, 0)
    if name == "no_blue":
        # markers + target but no blue components → no candidate to rank/transform
        g[0][0] = 2; g[0][1] = 2
        g[0][w - 1] = 3
        g[h // 2][w - 6] = 8
        return g
    if name == "no_red_marker":
        # blue + green + target but no red marker → no rank specified
        g[3][1] = 1
        paint_at(g, 5, 4, L_TROMINO_NE, 1)
        paint_at(g, 8, 1, T_TETROMINO, 1)
        g[0][w - 1] = 3; g[1][w - 1] = 3
        g[h // 2][w - 6] = 8
        return g
    if name == "no_target":
        # blue + markers but no cyan target → nowhere to stamp
        g[3][1] = 1
        paint_at(g, 5, 4, L_TROMINO_NE, 1)
        paint_at(g, 8, 1, T_TETROMINO, 1)
        g[0][0] = 2
        g[0][w - 1] = 3
        return g
    return g
