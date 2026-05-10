"""Generator for arc_puzzle_bank_21_set19_bundle:easy_p04 — reduce odd-length runs to centers.

Rule: horizontal odd-length runs are separated by zeros and reduce to
their centers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: even_length_runs, no_runs, length_1_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9afcb69acd1"
VERSION = "1.1.0"
TASK_ID = "b9afcb69acd1"
SUMMARY = "Horizontal odd-length runs are separated by zeros and reduce to their centers."

INVARIANTS = [
    "background is 0",
    "each active row has one solid monochrome run of length 3, 5, or 7",
    "runs are horizontal and isolated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("even_length_runs", "no_runs", "length_1_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "odd_length_runs",
                       "valid": "odd_length_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
        run_count = min(ctx.draw_int("run_count", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 13)
        run_count = min(ctx.draw_int("run_count", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 9, 13)
        run_count = min(ctx.draw_int("run_count", 2, 4), h)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)

    rows = rng.sample(range(h), run_count)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], run_count)
    allowed_lengths = [length for length in (3, 5, 7) if length <= w]
    for row, color in zip(rows, colors):
        length = rng.choice(allowed_lengths)
        c0 = rng.randint(0, w - length)
        for c in range(c0, c0 + length):
            grid[row][c] = color
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 6, 11
    g = full_grid(h, w, 0)
    if name == "even_length_runs":
        # all runs even-length → no unique center cell, rule's reduction is undefined
        for c in range(1, 5): g[1][c] = 4   # length 4
        for c in range(2, 8): g[3][c] = 6   # length 6
        return g
    if name == "no_runs":
        # blank → no runs to reduce
        return g
    if name == "length_1_runs":
        # all runs length-1 (singletons) → center is itself, rule has no observable effect
        g[1][2] = 4
        g[3][5] = 6
        g[4][8] = 3
        return g
    return g
