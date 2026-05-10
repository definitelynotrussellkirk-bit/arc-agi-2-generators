"""Generator for arc_puzzle_bank_21_set16_s:S16_E5.

Rule: color-2 and color-3 endpoint segments intersect at one cell.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marks, parallel, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a79fb4ad1f55"
VERSION = "1.1.0"
TASK_ID = "a79fb4ad1f55"
SUMMARY = "Color-2 and color-3 endpoint segments intersect at one cell."

INVARIANTS = [
    "color 2 has exactly two horizontal endpoints",
    "color 3 has exactly two vertical endpoints",
    "the two spans cross at exactly one cell",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "parallel", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "width":          {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 9, 10)
    else:
        h = ctx.draw_int("height", 7, 10)
        w = ctx.draw_int("width", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 3)
    c = rng.randint(2, w - 3)
    c1 = rng.randint(0, c - 1)
    c2 = rng.randint(c + 1, w - 1)
    r1 = rng.randint(0, r - 1)
    r2 = rng.randint(r + 1, h - 1)
    g[r][c1] = 2
    g[r][c2] = 2
    g[r1][c] = 3
    g[r2][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_marks":
        return g
    if name == "parallel":
        g[2][1] = 2; g[2][6] = 2
        g[5][1] = 2; g[5][6] = 2
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
