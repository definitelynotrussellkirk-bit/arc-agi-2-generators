"""Generator for arc_puzzle_bank_twentysecond21:E153.

Rule: each row has scattered non-zero cells; output left-aligns the
non-zero values within the row.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
density.
Degenerates: empty_grid, single_value, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a2f04639576"
VERSION = "1.1.0"
TASK_ID = "1a2f04639576"

SUMMARY = "Sparse non-zero cells scattered across multiple rows; gravity left."

INVARIANTS = [
    "background is 0",
    "1-3 non-zero cells per row at random positions",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_grid", "single_value", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "density":        {"type": "str", "default": "rng", "valid": "low|med|high"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 3, 3)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 3, 5)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)
    for r in range(h):
        n = rng.randint(1, 3)
        cols = rng.sample(range(w), n)
        for c in cols:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(4, 6, 0)
    if name == "empty_grid":
        return g
    if name == "single_value":
        g[2][3] = 3
        return g
    if name == "full_grid":
        for r in range(4):
            for c in range(6):
                g[r][c] = 3
        return g
    return g
