"""Generator for arc_additional_puzzle_bank_volume10:H70.

Rule: legend-mapped majority seed colors fill separated chambers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, seed_distribution, texture.
Degenerates: no_legend, no_walls, tied_majority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc4d84a0bbf4"
VERSION = "1.1.0"
TASK_ID = "fc4d84a0bbf4"
SUMMARY = "Legend-mapped majority seed colors fill separated chambers."

INVARIANTS = [
    "background is 0",
    "top two rows contain a seed-to-fill legend",
    "gray walls split the area below the legend into chambers",
    "each active chamber has a strict majority among seed colors 1, 2, and 3",
]

PALETTE_KINDS = ("default", "left_majority_1", "right_majority_2", "balanced")
DEGENERATE_TEXTURES = ("no_legend", "no_walls", "tied_majority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "9..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "split_chambers",
                       "valid": "split_chambers"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 16)
    g = full_grid(h, w, 0)
    for c, seed_color, fill_color in [(0, 1, 6), (1, 2, 7), (2, 3, 8)]:
        g[0][c] = seed_color
        g[1][c] = fill_color
    wall = w // 2
    for r in range(2, h):
        g[r][wall] = 5
    for r, c, v in [(3, 1, 1), (4, 2, 1), (h - 3, 2, 2),
                     (3, wall + 2, 3), (4, wall + 3, 3), (h - 3, wall + 2, 2)]:
        g[r][c] = v
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    wall = w // 2
    if name == "no_legend":
        # walls + seeds but no top-row legend → seed→fill mapping undefined
        for r in range(2, h):
            g[r][wall] = 5
        for r, c, v in [(3, 1, 1), (4, 2, 1), (3, wall + 2, 3)]:
            g[r][c] = v
        return g
    if name == "no_walls":
        # legend + seeds but no walls → no chambers, majority undefined
        for c, seed_color, fill_color in [(0, 1, 6), (1, 2, 7), (2, 3, 8)]:
            g[0][c] = seed_color; g[1][c] = fill_color
        for r, c, v in [(3, 1, 1), (4, 2, 1), (h - 3, 2, 2)]:
            g[r][c] = v
        return g
    if name == "tied_majority":
        # left chamber has tied counts of 1 and 2 → no strict majority
        for c, seed_color, fill_color in [(0, 1, 6), (1, 2, 7), (2, 3, 8)]:
            g[0][c] = seed_color; g[1][c] = fill_color
        for r in range(2, h):
            g[r][wall] = 5
        for r, c, v in [(3, 1, 1), (4, 2, 2), (5, 1, 1), (5, 2, 2)]:
            g[r][c] = v
        return g
    return g
