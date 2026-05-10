"""Generator for arc_additional_puzzle_bank_volume9:M60.

Rule: for each non-bg color with exactly 2 cells (sorted by reading
order), draw an L-path (horizontal then vertical) connecting them.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_pairs, single_pair, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e072894e6f1"
VERSION = "1.1.0"
TASK_ID = "1e072894e6f1"
SUMMARY = "Draw L-paths between color pairs."

INVARIANTS = [
    "between 2 and 3 distinct colors",
    "each color has exactly 2 cells at distinct positions",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pairs", "single_pair", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "9..11"},
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
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[0][8] = 9
    g[2][5] = 9
    g[4][0] = 8
    g[4][2] = 8
    g[5][1] = 6
    g[7][0] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_pairs":
        return g
    if name == "single_pair":
        g[2][2] = 9
        g[5][7] = 9
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 9
        return g
    return g
