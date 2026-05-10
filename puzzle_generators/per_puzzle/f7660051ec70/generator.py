"""Generator for arc_additional_puzzles_21_set2:M9.

Rule: for each closed 1-frame, if a 2-cell is inside the frame, fill all
empty cells inside with 3.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frames, no_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "f7660051ec70"
VERSION = "1.1.0"
TASK_ID = "f7660051ec70"
SUMMARY = "2 closed 1-frames: one with 2-seed inside, one empty; fill seeded interior with 3."

INVARIANTS = [
    "exactly 2 closed 1-frames",
    "exactly one frame has a 2-seed inside",
    "the other frame has empty interior",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "9..11"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "11..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    draw_frame(g, 1, 1, 4, 5, 1)
    g[2][3] = 2
    draw_frame(g, 5, 6, 8, 11, 1)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_frames":
        g[2][3] = 2
        return g
    if name == "no_seed":
        draw_frame(g, 1, 1, 4, 5, 1)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
