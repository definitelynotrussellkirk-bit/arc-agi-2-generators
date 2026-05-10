"""Generator for arc_puzzle_bank_seventh21:E49.

Rule: sparse left-half cells are copied to the right half by vertical
mirror.

Combinatorial axes (8): grid_h, half_w, cells, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_cells, all_left_half, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "32a376372541"
VERSION = "1.1.0"
TASK_ID = "32a376372541"
SUMMARY = "Sparse left-half cells are copied to the right half by vertical mirror."

INVARIANTS = [
    "background is 0",
    "grid width is even",
    "source cells are in the left half",
    "mirrored right-half cells are initially empty",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cells", "all_left_half", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "cells":          {"type": "int", "default": "rng 3..7", "valid": "1..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "left_half", "valid": "left_half"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("half_w", 4, 5) * 2
        target = ctx.draw_int("cells", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("half_w", 5, 6) * 2
        target = ctx.draw_int("cells", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("half_w", 4, 6) * 2
        target = ctx.draw_int("cells", 3, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    candidates = [(r, c) for r in range(h) for c in range(w // 2)]
    rng.shuffle(candidates)
    for r, c in candidates[:target]:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 10, 0)
    if name == "no_cells":
        return g
    if name == "all_left_half":
        for r in range(7):
            for c in range(5):
                g[r][c] = ((r + c) % 8) + 1
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
