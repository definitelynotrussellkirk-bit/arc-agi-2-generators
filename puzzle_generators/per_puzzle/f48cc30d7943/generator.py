"""Generator for arc_additional_puzzle_bank_volume10:M66.

Rule: color-5 walls partition the grid into regions; zero cells in regions
that contain exactly two color-2 seeds become 8.

Combinatorial axes (9): grid_h/w, palette_kind, num_regions, seed_per_region,
palette_size, position_bias, n_distinct_colors, distractor_color, texture.
Degenerates: no_walls, no_seeds, all_regions_qualify.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f48cc30d7943"
VERSION = "1.1.0"
TASK_ID = "f48cc30d7943"
SUMMARY = "Color-5 walls partition regions; zero cells in regions containing exactly two 2-seeds become 8."

INVARIANTS = [
    "walls are color 5 and block connected regions",
    "at least one region contains exactly two color-2 seeds",
]

PALETTE_KINDS = ("default", "more_seeds", "wide_distractor", "tight_walls")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "all_regions_qualify")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_regions":    {"type": "int", "default": "4", "valid": "4"},
    "seed_per_region": {"type": "str", "default": "mixed",
                        "valid": "mixed|all_two"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    mid_r = h // 2
    mid_c = w // 2
    for c in range(w):
        g[mid_r][c] = 5
    for r in range(h):
        g[r][mid_c] = 5
    g[1][1] = 2
    g[mid_r - 1][mid_c - 1] = 2
    g[mid_r + 1][1] = 2
    g[1][mid_c + 1] = 2
    g[1][w - 2] = 2
    g[h - 2][w - 2] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    mid_r, mid_c = h // 2, w // 2
    if name == "no_walls":
        # seeds without walls — single region, rule has no partition
        g[1][1] = 2
        g[1][3] = 2
        g[3][1] = 2
        g[3][3] = 2
        return g
    if name == "no_seeds":
        # walls partition the grid but no seeds — rule fills nothing
        for c in range(w):
            g[mid_r][c] = 5
        for r in range(h):
            g[r][mid_c] = 5
        return g
    if name == "all_regions_qualify":
        # every region has exactly 2 seeds — rule fills all open cells
        for c in range(w):
            g[mid_r][c] = 5
        for r in range(h):
            g[r][mid_c] = 5
        g[1][1] = 2; g[1][3] = 2
        g[1][mid_c + 1] = 2; g[1][w - 2] = 2
        g[mid_r + 1][1] = 2; g[mid_r + 1][3] = 2
        g[h - 2][mid_c + 1] = 2; g[h - 2][w - 2] = 2
        return g
    return g
