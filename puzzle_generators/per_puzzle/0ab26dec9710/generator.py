"""Generator for arc_puzzle_bank_21_set8_s:S8_E1.

Each active row has multiple runs; only the unique longest run is kept.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, single_run_per_row, tied_run_lengths.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ab26dec9710"
VERSION = "1.1.0"
TASK_ID = "0ab26dec9710"

SUMMARY = "Each active row has multiple runs; only the unique longest run is kept."

INVARIANTS = [
    "background is 0",
    "two to five rows contain two separated same-color or different-color runs",
    "each active row has a unique longest run",
    "outputs preserve only the longest run in each active row",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "single_run_per_row", "tied_run_lengths")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "rows_with_two_runs",
                       "valid": "rows_with_two_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "1..6"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        active = min(ctx.draw_int("active_rows", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 14)
        active = min(ctx.draw_int("active_rows", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 10, 14)
        active = min(ctx.draw_int("active_rows", 2, 5), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), active)
    palette = [2, 3, 4, 6, 7, 9]
    for idx, r in enumerate(rows):
        long_len = rng.randint(4, min(6, w - 3))
        short_len = rng.randint(1, min(3, long_len - 1))
        if rng.random() < 0.5:
            c_long, c_short = 1, w - short_len - 1
        else:
            c_short, c_long = 1, w - long_len - 1
        _fill_run(g, r, c_long, long_len, palette[idx % len(palette)])
        _fill_run(g, r, c_short, short_len, palette[(idx + 2) % len(palette)])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 12
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank → no runs to compare
        return g
    if name == "single_run_per_row":
        # only one run per row → no longest-vs-shortest contrast
        _fill_run(g, 1, 1, 5, 4)
        _fill_run(g, 3, 1, 4, 6)
        return g
    if name == "tied_run_lengths":
        # two runs of equal length → "unique longest" precondition fails
        _fill_run(g, 2, 1, 3, 4)
        _fill_run(g, 2, 7, 3, 6)
        return g
    return g
