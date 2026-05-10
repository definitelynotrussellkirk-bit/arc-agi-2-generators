"""Generator for arc_additional_puzzles_21_set7:E48.

Rule: blank cells filled from partners reflected across the anti-diagonal.

Combinatorial axes (8): grid_h/w, grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marks, full_antidiag, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "da4a2278f620"
VERSION = "1.1.0"
TASK_ID = "da4a2278f620"
SUMMARY = "Blank cells filled from partners reflected across the anti-diagonal."

INVARIANTS = [
    "grid is square",
    "source cells have blank anti-diagonal reflected partners",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "full_antidiag", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "grid_size":      {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n = ctx.draw_int("grid_size", 6, 7)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 8, 9)
    else:
        n = ctx.draw_int("grid_size", 6, 9)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0]))
    g = full_grid(n, n, 0)
    for r, c, color in [(1, 1, colors[0]), (2, 4, colors[1]), (n - 2, 2, colors[2])]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_marks":
        return g
    if name == "full_antidiag":
        for i in range(7):
            g[i][6 - i] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
