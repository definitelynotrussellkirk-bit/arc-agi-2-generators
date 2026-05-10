"""Generator for arc_additional_puzzles_21_set14_bundle:M93.

Rule: color-8 walls partition rooms; each non-wall seed floods its
room with its color.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_seeds, no_walls, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef65ec3491d7"
VERSION = "1.1.0"
TASK_ID = "ef65ec3491d7"
SUMMARY = "Color-8 walls partition rooms; each non-wall seed floods its room with its color."

INVARIANTS = [
    "walls use color 8",
    "each room has exactly one seed color other than 0 or 8",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "corners", "valid": "corners"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    colors = list(ctx.draw_distinct_colors("seeds", n=4, exclude=[0, 8]))
    g = full_grid(h, w, 0)
    sr = h // 2
    sc = w // 2
    for c in range(w):
        g[sr][c] = 8
    for r in range(h):
        g[r][sc] = 8
    g[1][1] = colors[0]
    g[1][w - 2] = colors[1]
    g[h - 2][1] = colors[2]
    g[h - 2][w - 2] = colors[3]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_seeds":
        for c in range(10):
            g[5][c] = 8
        for r in range(10):
            g[r][5] = 8
        return g
    if name == "no_walls":
        g[1][1] = 2; g[1][8] = 3
        g[8][1] = 4; g[8][8] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
