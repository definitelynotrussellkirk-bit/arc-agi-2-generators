"""Generator for arc_puzzle_bank_21_set8_s:S8_E2 — odd-length runs reduce to midpoint.

Rule: every odd-length horizontal run is reduced to its midpoint cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: even_length_runs, no_runs, length_1_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2fc4ca4ea6c4"
VERSION = "1.1.0"
TASK_ID = "2fc4ca4ea6c4"

SUMMARY = "Every odd-length horizontal run is reduced to its midpoint cell."

INVARIANTS = [
    "background is 0",
    "all horizontal runs have odd length",
    "runs are separated within each row",
    "outputs keep only each run midpoint in the run color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("even_length_runs", "no_runs", "length_1_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_rows":       {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "row_runs_odd",
                       "valid": "row_runs_odd"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _fill_run(g, r, c0, length, color):
    for c in range(c0, c0 + length):
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
        run_rows = min(ctx.draw_int("run_rows", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 13)
        run_rows = min(ctx.draw_int("run_rows", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 9, 13)
        run_rows = min(ctx.draw_int("run_rows", 2, 5), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), run_rows)
    palette = [2, 3, 4, 6, 7]
    for idx, r in enumerate(rows):
        length = rng.choice([3, 5])
        c0 = rng.randint(0, w - length)
        _fill_run(g, r, c0, length, palette[idx % len(palette)])
        if c0 + length + 4 <= w and rng.random() < 0.5:
            _fill_run(g, r, c0 + length + 1, 3, palette[(idx + 2) % len(palette)])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "even_length_runs":
        # all runs even length → "midpoint" undefined / rule has no fixed point
        _fill_run(g, 1, 1, 4, 3)   # length 4 (even)
        _fill_run(g, 3, 2, 2, 6)   # length 2 (even)
        return g
    if name == "no_runs":
        # blank → no runs to reduce
        return g
    if name == "length_1_runs":
        # all runs already length 1 → rule is identity (already at midpoint)
        g[1][2] = 4
        g[2][5] = 6
        g[4][7] = 7
        return g
    return g
