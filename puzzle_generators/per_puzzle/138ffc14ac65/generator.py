"""Generator for arc_puzzle_bank_21_set4_d:easy_d02.

Rule: each seed paints its own column upward to the top edge.

Combinatorial axes (8): grid_h/w, seed_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_seeds, all_top_row, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "138ffc14ac65"
VERSION = "1.1.0"
TASK_ID = "138ffc14ac65"
SUMMARY = "Each seed paints its own column upward to the top edge."

INVARIANTS = [
    "background is 0",
    "seeds have distinct columns",
    "each nonzero seed is a singleton",
    "output keeps seed colors while filling upward",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "all_top_row", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "seed_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
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
        w = ctx.draw_int("grid_w", 6, 8)
        max_count = 3
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        max_count = 4
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 6, 10)
        max_count = 4
    count = ctx.draw_int("seed_count", 2, min(max_count, w))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], count)
    for c, color in zip(rng.sample(range(w), count), colors):
        g[rng.randint(1, h - 1)][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 8, 0)
    if name == "no_seeds":
        return g
    if name == "all_top_row":
        for c in range(8):
            g[0][c] = (c % 8) + 1
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(8):
                g[r][c] = 3
        return g
    return g
