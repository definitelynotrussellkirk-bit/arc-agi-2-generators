"""Generator for arc_puzzle_bank_21_set10_e:easy_j06.

Rule: for each horizontal run of same color, keep cells at even
positions in the run (dashed pattern); zero out odd positions.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, run_length, texture.
Degenerates: no_runs, length_2_run, all_runs_full_width.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cbbecffcd70e"
VERSION = "1.1.0"
TASK_ID = "cbbecffcd70e"
SUMMARY = "2-3 horizontal solid runs of length ≥3 in distinct colors."

INVARIANTS = [
    "≥2 horizontal runs of length ≥3",
    "runs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "length_2_run", "all_runs_full_width")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "run_length":     {"type": "str", "default": "rng_3_to_6", "valid": "rng_3_to_6"},
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
        length = rng.randint(3, min(w, 6))
        c0 = rng.randint(0, w - length)
        for i in range(length):
            g[r][c0 + i] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # empty grid — no horizontal runs to dash
        return g
    if name == "length_2_run":
        # length-2 run → "dashed" pattern keeps only first cell, drops second
        g[2][2] = 4; g[2][3] = 4
        g[4][1] = 6; g[4][2] = 6
        return g
    if name == "all_runs_full_width":
        # runs span the entire row → dashing produces a long alternating pattern
        for c in range(w):
            g[2][c] = 4
        for c in range(w):
            g[4][c] = 6
        return g
    return g
