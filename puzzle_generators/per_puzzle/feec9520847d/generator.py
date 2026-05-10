"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p06.

Rule: horizontal monochrome runs are reduced to their middle cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, even_length_runs, vertical_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "feec9520847d"
VERSION = "1.1.0"
TASK_ID = "feec9520847d"
SUMMARY = "Separated horizontal monochrome runs of varied lengths."

INVARIANTS = [
    "background is 0",
    "all nonzero cells belong to horizontal runs",
    "runs are separated by zeros",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "even_length_runs", "vertical_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_runs",
                       "valid": "row_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        run_count = ctx.draw_int("run_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        run_count = ctx.draw_int("run_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        run_count = ctx.draw_int("run_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=run_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            length = rng.randint(2, min(6, w))
            r = rng.randrange(h)
            c = rng.randint(0, w - length)
            band = range(max(0, c - 1), min(w, c + length + 1))
            if all(g[r][cc] == 0 for cc in band):
                for cc in range(c, c + length):
                    g[r][cc] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # length-1 runs only → "middle of a 1-cell run" is identity, rule has no effect
        g[1][2] = 4; g[3][6] = 6; g[5][1] = 3; g[5][8] = 8
        return g
    if name == "even_length_runs":
        # length-2/4 runs → no integer middle (ambiguous which cell to keep)
        for c in range(1, 3): g[1][c] = 4   # length 2
        for c in range(4, 8): g[3][c] = 6   # length 4
        for c in range(2, 6): g[5][c] = 3   # length 4
        return g
    if name == "vertical_runs":
        # vertical runs (col-aligned) → rule scans rows, sees only length-1 horizontal runs
        for r in range(1, 4): g[r][2] = 4
        for r in range(2, 6): g[r][7] = 6
        for r in range(4, 7): g[r][9] = 3
        return g
    return g
