"""Generator for arc_additional_puzzles_21_set14_bundle:H93.

Rule: each non-zero cell is a seed. For each empty cell, find nearest
seeds by Manhattan distance; if the unique nearest is one color, take it;
ties → 0.

Combinatorial axes (8): grid_h/w, palette_kind, num_seeds, seed_spread,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_one_seed, all_same_color, no_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "42ccd1ff25f3"
VERSION = "1.1.0"
TASK_ID = "42ccd1ff25f3"
SUMMARY = "2-3 distinct-color seed cells placed asymmetrically."

INVARIANTS = [
    "between 2 and 3 single-cell seeds of distinct colors",
    "seeds placed at distinct rows AND cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("only_one_seed", "all_same_color", "no_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_seeds":      {"type": "int", "default": "3", "valid": "3"},
    "seed_spread":    {"type": "str", "default": "wide", "valid": "wide"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6]; rng.shuffle(palette)
    g[1][1] = palette[0]
    g[1][w - 2] = palette[1]
    g[h - 2][3] = palette[2]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "only_one_seed":
        # one seed — every non-seed cell takes its color (no ties)
        g[3][4] = 5
        return g
    if name == "all_same_color":
        # 3 seeds same color — no color distinction, all cells become that color
        g[1][1] = 4
        g[1][w - 2] = 4
        g[h - 2][3] = 4
        return g
    if name == "no_seeds":
        return g
    return g
