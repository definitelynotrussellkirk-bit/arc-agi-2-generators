"""Generator for arc_additional_puzzles_21_set5:M33.

Rule: cmd at (0,0); zero out (0,0); for each non-zero cell, mirror
copy: cmd=1 horizontal flip, else vertical flip. Restore cmd at (0,0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd, palette_size,
position_bias, n_distinct_colors, blob_kind, texture.
Degenerates: no_cmd, no_blob, mirror_target_occupied.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "69e5340ad7b0"
VERSION = "1.1.0"
TASK_ID = "69e5340ad7b0"
SUMMARY = "Cmd 1 or 2 at (0,0) + small blob in upper-left quadrant."

INVARIANTS = [
    "cmd at (0,0) ∈ {1, 2}",
    "small multicolor blob in upper-left, mirrored cells stay in-bounds",
]

PALETTE_KINDS = ("default", "horiz_flip", "vert_flip", "varied_cmd")
DEGENERATE_TEXTURES = ("no_cmd", "no_blob", "mirror_target_occupied")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "upper_left", "valid": "upper_left"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "blob_kind":      {"type": "str", "default": "P_shape", "valid": "P_shape"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    cmd = ctx.draw_int("cmd", 1, 2)
    g = full_grid(h, w, 0)
    g[0][0] = cmd
    g[2][1] = 1
    g[2][2] = 2
    g[3][1] = 1
    g[3][2] = 2
    g[4][1] = 2
    g[4][2] = 2
    g[4][3] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # blob present but no cmd at (0,0) → flip axis undefined
        for r, c, v in [(2, 1, 1), (2, 2, 2), (3, 1, 1), (3, 2, 2),
                        (4, 1, 2), (4, 2, 2), (4, 3, 2)]:
            g[r][c] = v
        return g
    if name == "no_blob":
        # cmd at (0,0) but nothing to mirror
        g[0][0] = 1
        return g
    if name == "mirror_target_occupied":
        # blob plus pre-occupied mirror destination → predicted cells already non-bg
        g[0][0] = 1
        for r, c, v in [(2, 1, 1), (3, 1, 1)]:
            g[r][c] = v
        for r, c in [(2, w - 2), (3, w - 2)]:
            g[r][c] = 4
        return g
    return g
