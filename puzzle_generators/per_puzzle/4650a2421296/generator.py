"""Generator for arc_additional_puzzle_bank_volume16:M108.

Rule: the gray-wall chamber with the most red seeds is filled cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, seed_distribution, texture.
Degenerates: no_seeds, no_walls, tied_seed_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4650a2421296"
VERSION = "1.1.0"
TASK_ID = "4650a2421296"
SUMMARY = "The gray-wall chamber with the most red seeds is filled cyan."

INVARIANTS = [
    "background is 0",
    "gray walls partition the board into chambers",
    "one chamber has strictly more red seeds than all others",
    "selected chamber contains blank cells to fill",
]

PALETTE_KINDS = ("default", "left_winner", "right_winner", "balanced_close")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "tied_seed_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "chamber", "valid": "chamber"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "seed_distribution": {"type": "str", "default": "skewed", "valid": "skewed"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 10, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    wall = rng.randint(4, w - 5)
    for r in range(1, h - 1):
        g[r][wall] = 5
    for r, c in [(1, 1), (2, 2), (h - 3, 2)]:
        g[r][c] = 2
    g[1][wall + 1] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # walls + chambers but no red seeds → no chamber to fill
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(1, h - 1):
            g[r][5] = 5
        return g
    if name == "no_walls":
        # red seeds but no gray walls → no chamber boundary
        for r, c in [(1, 1), (2, 2), (4, 6), (5, 8)]:
            g[r][c] = 2
        return g
    if name == "tied_seed_counts":
        # both chambers have the same number of red seeds → "most" is undefined
        for r in range(h):
            g[r][0] = 5; g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5; g[h - 1][c] = 5
        for r in range(1, h - 1):
            g[r][5] = 5
        for r, c in [(1, 1), (2, 2)]:
            g[r][c] = 2
        for r, c in [(1, 8), (2, 9)]:
            g[r][c] = 2
        return g
    return g
