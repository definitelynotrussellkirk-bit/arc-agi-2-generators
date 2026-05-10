"""Generator for arc_additional_puzzles_21_set21_bundle:M141.

Rule: row 0 has 2 palette colors. 1-frame contains 9-seed. From seed
in all 4 cardinal directions, paint cells (alternating palette) until
walls.

Combinatorial axes (8): grid_h/w, palette_kind, frame_size,
palette_size, position_bias, n_distinct_colors, seed_pos, texture.
Degenerates: no_palette, no_frame, no_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "0f0d405d5bb8"
VERSION = "1.1.0"
TASK_ID = "0f0d405d5bb8"
SUMMARY = "Row 0 has 2 palette colors + 1-frame inside body containing 9-seed."

INVARIANTS = [
    "row 0 has 2 palette cells",
    "1-frame in body with 9-seed inside",
]

PALETTE_KINDS = ("default", "warm_palette", "cool_palette", "varied_palette")
DEGENERATE_TEXTURES = ("no_palette", "no_frame", "no_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_size":     {"type": "str", "default": "fit_grid",
                       "valid": "fit_grid"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "centered",
                       "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "seed_pos":       {"type": "str", "default": "center", "valid": "center"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8]; rng.shuffle(palette)
    g[0][1] = palette[0]; g[0][2] = palette[1]
    draw_frame(g, 1, 1, h - 2, w - 2, 1)
    g[h // 2][w // 2] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # frame + seed but no palette → alternation source undefined
        draw_frame(g, 1, 1, h - 2, w - 2, 1)
        g[h // 2][w // 2] = 9
        return g
    if name == "no_frame":
        # palette + seed but no 1-frame → no walls to bound rays
        g[0][1] = 4; g[0][2] = 6
        g[h // 2][w // 2] = 9
        return g
    if name == "no_seed":
        # palette + frame but no 9-seed → no rays generated
        g[0][1] = 4; g[0][2] = 6
        draw_frame(g, 1, 1, h - 2, w - 2, 1)
        return g
    return g
