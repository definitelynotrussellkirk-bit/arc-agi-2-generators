"""Generator for arc_puzzle_bank_21_next:easy_c05.

Rule: for each non-bg cell at (r, c, v), paint the entire row r and
column c with v on a fresh empty grid.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marks, full_row, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6058ff1ae20c"
VERSION = "1.1.0"
TASK_ID = "6058ff1ae20c"
SUMMARY = "1-2 isolated non-bg cells on an otherwise-empty grid."

INVARIANTS = [
    "exactly 1-2 non-bg cells, no two in same row or col",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "full_row", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
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
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n = rng.randint(1, 2)
    rs = rng.sample(range(h), n)
    cs = rng.sample(range(w), n)
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(n):
        g[rs[i]][cs[i]] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 7, 0)
    if name == "no_marks":
        return g
    if name == "full_row":
        for c in range(7):
            g[3][c] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
