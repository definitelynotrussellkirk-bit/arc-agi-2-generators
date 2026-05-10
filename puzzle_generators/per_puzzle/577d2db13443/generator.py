"""Generator for arc_puzzle_bank_21_set9_s:S9_E3.

Rule: horizontal runs are preserved except their two endpoints are
recolored to 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, run_length, texture.
Degenerates: no_runs, length_2_run, run_with_color_1.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "577d2db13443"
VERSION = "1.1.0"
TASK_ID = "577d2db13443"
SUMMARY = "Horizontal runs are preserved except their two endpoints are recolored to 1."

INVARIANTS = [
    "background is 0",
    "there are two to four horizontal same-color runs",
    "each run has length at least three",
    "runs are separated by blank rows or columns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "length_2_run", "run_with_color_1")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "run_length":     {"type": "str", "default": "≥3", "valid": "≥3"},
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
        w = ctx.draw_int("grid_w", 8, 10)
        count = min(ctx.draw_int("run_count", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        count = min(ctx.draw_int("run_count", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        count = min(ctx.draw_int("run_count", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), count)
    colors = [2, 3, 4, 6, 7, 8]
    for r, color in zip(rows, colors):
        length = rng.randint(3, min(5, w))
        c0 = rng.randint(0, w - length)
        for c in range(c0, c0 + length):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # empty grid — no runs to recolor
        return g
    if name == "length_2_run":
        # length-2 run → "endpoint" is every cell; rule recolors entire run
        g[2][2] = 4; g[2][3] = 4
        return g
    if name == "run_with_color_1":
        # run already uses color 1 → endpoints recoloring is invisible
        g[2][1] = 1; g[2][2] = 1; g[2][3] = 1; g[2][4] = 1
        return g
    return g
