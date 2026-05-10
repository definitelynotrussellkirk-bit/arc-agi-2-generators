"""Generator for arc_puzzle_bank_21_set15_bundle:easy_o01.

Odd-length horizontal runs are reduced to their central cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, all_singletons, even_length_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5000bcb83fa9"
VERSION = "1.1.0"
TASK_ID = "5000bcb83fa9"
SUMMARY = "Separated odd-length horizontal runs of nonzero colors."

INVARIANTS = [
    "background is 0",
    "all nonzero cells belong to odd-length horizontal runs",
    "runs are separated by zeros",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "all_singletons", "even_length_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "separated_horizontal_runs",
                       "valid": "separated_horizontal_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 9, 11)
        run_count = ctx.draw_int("run_count", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
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
            length = rng.choice([1, 3, 5])
            if length > w:
                continue
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
    if name == "no_runs":
        # blank → no runs to reduce
        return g
    if name == "all_singletons":
        # all length-1 runs → every cell is already its own center (rule = identity)
        g[1][2] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    if name == "even_length_runs":
        # even-length runs have no unique center → rule's "central cell" precondition fails
        g[1][1] = 4; g[1][2] = 4
        g[3][4] = 6; g[3][5] = 6; g[3][6] = 6; g[3][7] = 6
        return g
    return g
