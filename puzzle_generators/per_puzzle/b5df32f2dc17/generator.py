"""Generator for arc_puzzle_bank_21_set8_s:S8_M1 — sort runs by length.

Rule: in each row, find non-zero runs (color + length). Sort the runs
by descending length, place left-to-right in the row with 1-cell
separator gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, single_run, tied_lengths.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5df32f2dc17"
VERSION = "1.1.0"
TASK_ID = "b5df32f2dc17"
SUMMARY = "3-4 rows, each with 2-3 runs of different colors (lengths vary)."

INVARIANTS = [
    "background is 0",
    "each row has 2-3 runs of distinct colors and strictly distinct lengths",
    "runs are separated by at least one 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "single_run", "tied_lengths")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_runs",
                       "valid": "row_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 3, 4)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 3, 5)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        n_runs = rng.randint(2, 3)
        lengths = rng.sample(range(2, 5), n_runs)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_runs)
        c = rng.randint(0, 1)
        for length, color in zip(lengths, colors):
            if c + length > w:
                break
            for k in range(length):
                g[r][c + k] = color
            c += length + rng.randint(1, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 12
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank row → no runs to sort
        return g
    if name == "single_run":
        # only one run per row → sort is identity
        for k in range(3): g[0][k] = 4
        for k in range(2): g[2][k] = 6
        return g
    if name == "tied_lengths":
        # multiple runs with equal length → ambiguous "longest"
        for k in range(2): g[0][k] = 3
        for k in range(2): g[0][4 + k] = 6
        for k in range(2): g[0][8 + k] = 7
        return g
    return g
