"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p01.

Rule: columns contain two same-color endpoints with an empty vertical
span; the gap is filled with the endpoint color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, span_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, endpoints_adjacent, single_endpoint_per_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "caa7a75c44ad"
VERSION = "1.1.0"
TASK_ID = "caa7a75c44ad"
SUMMARY = "Columns contain two same-color endpoints with an empty vertical span."

INVARIANTS = [
    "background is 0",
    "each active column has exactly two nonzero cells",
    "the two cells in an active column share one color and have only zeros between them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "endpoints_adjacent", "single_endpoint_per_col")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "span_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "column_pairs",
                       "valid": "column_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 6, 7)
        span_count = min(ctx.draw_int("span_count", 2, 2), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 9, 10)
        span_count = min(ctx.draw_int("span_count", 3, 4), w)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 6, 10)
        span_count = min(ctx.draw_int("span_count", 2, 4), w)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)

    cols = rng.sample(range(w), span_count)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], span_count)
    for col, color in zip(cols, colors):
        gap = rng.randint(1, max(1, min(5, h - 2)))
        r1 = rng.randint(0, h - gap - 1)
        r2 = r1 + gap
        grid[r1][col] = color
        grid[r2][col] = color
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 8
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # empty grid → no col pairs to fill
        return g
    if name == "endpoints_adjacent":
        # endpoints touching → no vertical span between them
        g[2][1] = 4; g[3][1] = 4
        g[5][5] = 6; g[6][5] = 6
        return g
    if name == "single_endpoint_per_col":
        # one marker per column → no second endpoint
        g[2][1] = 4
        g[5][5] = 6
        return g
    return g
