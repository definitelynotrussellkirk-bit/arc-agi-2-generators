"""Generator for arc_puzzle_bank_21_set10_e:easy_j05.

Rule: for each horizontal run of same color, paint cell to left of
start (if 0) and cell to right of end (if 0) with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, run_at_edge, vertical_runs_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d19cd1698b1"
VERSION = "1.1.0"
TASK_ID = "6d19cd1698b1"
SUMMARY = "2-3 horizontal solid runs in distinct colors with empty flanks."

INVARIANTS = [
    "≥2 horizontal runs with empty cells on both sides",
    "runs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "run_at_edge", "vertical_runs_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "row_local", "valid": "row_local"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n = rng.randint(2, 3)
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n)
    used_rows = rng.sample(range(h), n)
    for color, r in zip(pal, used_rows):
        length = rng.randint(2, 4)
        c0 = rng.randint(1, w - length - 1)
        for i in range(length):
            g[r][c0 + i] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # empty grid → no runs to grow, output equals input
        return g
    if name == "run_at_edge":
        # run starts at col 0 / ends at col w-1 → left/right flank is out-of-bounds
        for c in range(0, 3):
            g[1][c] = 3
        for c in range(w - 4, w):
            g[3][c] = 5
        return g
    if name == "vertical_runs_only":
        # color cells are vertically aligned → no horizontal runs to grow
        for r in range(2, 5):
            g[r][3] = 6
        for r in range(1, 4):
            g[r][7] = 4
        return g
    return g
