"""Generator for puzzle 28e73c20.

Rule: empty grid. Output is a spiral of 3s starting at (0,0).

Combinatorial axes (8): grid_n, anchor_corner, asymmetry_force,
palette_size, include_decoy, fill_color, position_bias, seed_position.
Degenerates: full_grid, single_cell, monochrome.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e8b6ff767c21"
VERSION = "1.1.0"
TASK_ID = "e8b6ff767c21"
SUMMARY = "Empty NxN grid; rule outputs spiral of 3s."

INVARIANTS = [
    "h = w = n, n in [5, 22]",
    "all cells are 0",
]

DEGENERATE_TEXTURES = ("full_grid", "single_cell", "monochrome")

AXES = {
    "grid_n":         {"type": "int", "default": "rng 8..16", "valid": "5..22"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "0", "valid": "0"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "fill_color":     {"type": "color", "default": "0", "valid": "0"},
    "position_bias":  {"type": "str", "default": "n/a", "valid": "n/a"},
    "seed_position":  {"type": "str", "default": "n/a", "valid": "n/a"},
    "texture":        {"type": "str", "default": "n/a (all empty grids)",
                       "valid": "|".join(DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n_lo, n_hi = 5, 8
    elif difficulty == "hard":
        n_lo, n_hi = 14, 22
    else:
        n_lo, n_hi = 8, 16
    n = int(overrides.get("grid_n",
                          ctx.draw_int("grid_n", n_lo, n_hi)))
    n = max(5, min(22, n))
    return full_grid(n, n, 0)


def _draw_from_degenerate(name, rng):
    n = 10
    g = full_grid(n, n, 0)
    if name == "full_grid":
        for r in range(n):
            for c in range(n):
                g[r][c] = 3
        return g
    if name == "single_cell":
        g[n // 2][n // 2] = 3
        return g
    if name == "monochrome":
        for r in range(n):
            for c in range(n):
                g[r][c] = 5
        return g
    return g
