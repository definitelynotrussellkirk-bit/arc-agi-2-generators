"""Generator for arc_puzzle_bank_21_next:medium_c02.

Rule: keep objects that are exactly rectangle frames (h≥3, w≥3, all
cells on bbox border). Drop solid rectangles and irregular shapes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, all_frames, all_solid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "54875f792be0"
VERSION = "1.1.0"
TASK_ID = "54875f792be0"
SUMMARY = "1-2 frame-shaped objects + 1-2 non-frame distractors."

INVARIANTS = [
    "exactly 1-2 frame objects (h≥3, w≥3, hollow border)",
    "1-2 non-frame distractors (solid rectangles or irregular)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "all_frames", "all_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "frames_left_distractors_right",
                       "valid": "frames_left_distractors_right"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_solid(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    draw_frame(g, 1, 1, 4, 5, 2)
    _draw_solid(g, 1, 7, 2, 8, 6)
    g[5][7] = 7; g[5][8] = 7; g[6][7] = 7; g[7][7] = 7; g[7][8] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # only solid + irregular → rule keeps nothing
        _draw_solid(g, 1, 1, 3, 3, 4)
        g[5][5] = 6; g[5][6] = 6; g[6][6] = 6
        return g
    if name == "all_frames":
        # only frames → rule keeps everything (identity)
        draw_frame(g, 1, 1, 4, 5, 2)
        draw_frame(g, 5, 7, 4, 5, 6)
        return g
    if name == "all_solid":
        # only solid rectangles → rule drops everything, output empty
        _draw_solid(g, 1, 1, 3, 4, 4)
        _draw_solid(g, 5, 6, 8, 9, 6)
        return g
    return g
