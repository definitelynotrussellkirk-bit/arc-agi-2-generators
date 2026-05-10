"""Generator for arc_puzzle_bank_tenth21:E68.

Rule: rows with one odd color recolor that cell to the row majority.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marks, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "40b155c46f6e"
VERSION = "1.1.0"
TASK_ID = "40b155c46f6e"
SUMMARY = "Rows with one odd color recolor that cell to the row majority."

INVARIANTS = [
    "background is 0",
    "each active row has exactly two nonzero colors",
    "one color appears once and the other appears multiple times",
    "inactive cells stay zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        majority, odd = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
        n_major = rng.randint(2, min(5, w - 1))
        cols = rng.sample(range(w), n_major + 1)
        for c in cols[:-1]:
            g[r][c] = majority
        g[r][cols[-1]] = odd
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 9, 0)
    if name == "no_marks":
        return g
    if name == "single_color":
        for r in range(6):
            for c in range(2, 7):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(9):
                g[r][c] = 3
        return g
    return g
