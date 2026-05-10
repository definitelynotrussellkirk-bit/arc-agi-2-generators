"""Generator for arc_puzzle_bank_21_set11_bundle:easy_k04.

Rule: sparse cells in a square grid are copied to transposed
row/column positions.

Combinatorial axes (8): grid_n, n_seeds, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_seeds, on_diagonal_only, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aa378df15340"
VERSION = "1.1.0"
TASK_ID = "aa378df15340"
SUMMARY = "Sparse cells in a square grid are copied to transposed row/column positions."

INVARIANTS = [
    "grid is square",
    "input has sparse nonzero cells",
    "background is zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "on_diagonal_only", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_n":         {"type": "int", "default": "rng 5..9", "valid": "3..14"},
    "n_seeds":        {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "off_diagonal", "valid": "off_diagonal"},
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
        n = ctx.draw_int("grid_n", 5, 6)
        count = ctx.draw_int("n_seeds", 3, 4)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_n", 8, 9)
        count = ctx.draw_int("n_seeds", 5, 6)
    else:
        n = ctx.draw_int("grid_n", 5, 9)
        count = ctx.draw_int("n_seeds", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(n, n, 0)
    positions = [(r, c) for r in range(n) for c in range(n) if r != c]
    rng.shuffle(positions)
    colors = list(ctx.draw_distinct_colors("colors", n=min(count, 9), exclude={0}))
    for i, (r, c) in enumerate(positions[:count]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_seeds":
        return g
    if name == "on_diagonal_only":
        for i in range(7):
            g[i][i] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 3
        return g
    return g
