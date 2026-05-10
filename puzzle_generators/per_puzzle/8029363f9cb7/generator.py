"""Generator for arc_additional_puzzle_bank_volume14:H95.

Rule: walking ray inside 5-frame; same as H100 but 2-source instead of
1, with bouncing on 3/4 deflectors and 5-frame walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, deflect_col,
deflect_row, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_source, no_deflectors, source_outside_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8029363f9cb7"
VERSION = "1.1.0"
TASK_ID = "8029363f9cb7"
SUMMARY = "5-frame surrounding interior + 2-source + 3-deflector + 4-deflector."

INVARIANTS = [
    "5-frame on outer border",
    "exactly one 2-source on left side of interior",
    "1-2 deflectors (color 3 or 4) along the ray's path",
]

PALETTE_KINDS = ("default", "high_deflect", "low_deflect", "mid_deflect")
DEGENERATE_TEXTURES = ("no_source", "no_deflectors", "source_outside_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "deflect_col":    {"type": "int", "default": "rng 4..7", "valid": "4..7"},
    "deflect_row":    {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "frame_relative", "valid": "frame_relative"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    h, w = 8, 12
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    g[1][1] = 2
    if difficulty == "easy":
        deflect_col = ctx.draw_int("deflect_col", 4, 5)
        deflect_row = ctx.draw_int("deflect_row", 3, 4)
    elif difficulty == "hard":
        deflect_col = ctx.draw_int("deflect_col", 6, 7)
        deflect_row = ctx.draw_int("deflect_row", 4, 5)
    else:
        deflect_col = ctx.draw_int("deflect_col", 4, 7)
        deflect_row = ctx.draw_int("deflect_row", 3, 5)
    g[1][deflect_col] = 4
    g[deflect_row][deflect_col] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    if name == "no_source":
        # frame + deflectors but no 2-source → ray has no origin
        g[1][5] = 4
        g[3][5] = 3
        return g
    if name == "no_deflectors":
        # frame + source but no deflectors → ray runs straight to opposite wall
        g[1][1] = 2
        return g
    if name == "source_outside_frame":
        # 2-source on the frame border itself → ray's interior position invalid
        g[0][1] = 2
        g[1][5] = 4
        g[3][5] = 3
        return g
    return g
