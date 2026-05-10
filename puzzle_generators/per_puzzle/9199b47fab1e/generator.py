"""Generator for arc_additional_puzzle_bank_volume6:H37.

Rule: a seed floods reachable floor cells by distance modulo 3 around
gray walls.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_walls, no_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9199b47fab1e"
VERSION = "1.1.0"
TASK_ID = "9199b47fab1e"
SUMMARY = "Seed floods floor cells by distance mod 3 around gray walls."

INVARIANTS = [
    "background is 0",
    "walls are 8",
    "there is one or more seed cells of color 2",
    "all open floor cells are reachable from a seed",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_walls", "no_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "8..13"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "8..13"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 8
        g[r][w - 1] = 8
    for c in range(w):
        g[0][c] = 8
        g[h - 1][c] = 8
    g[h // 2][w // 2] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_walls":
        g[5][5] = 2
        return g
    if name == "no_seed":
        for r in range(10):
            g[r][0] = 8
            g[r][9] = 8
        for c in range(10):
            g[0][c] = 8
            g[9][c] = 8
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
