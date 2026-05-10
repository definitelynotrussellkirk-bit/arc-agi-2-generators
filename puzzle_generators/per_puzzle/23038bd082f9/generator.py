"""Generator for arc_puzzle_bank_21_set21_bundle:easy_p01.

Rule: rows contain two same-color endpoints with an empty span between
them; the gap gets filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, span_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, endpoints_adjacent, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "23038bd082f9"
VERSION = "1.1.0"
TASK_ID = "23038bd082f9"
SUMMARY = "Rows contain two same-color endpoints with an empty span between them."

INVARIANTS = [
    "background is 0",
    "each active row has exactly two nonzero cells",
    "the active row endpoints share one color and have only zeros between them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "endpoints_adjacent", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "span_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row_pairs",
                       "valid": "row_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 10)
        span_count = min(ctx.draw_int("span_count", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        span_count = min(ctx.draw_int("span_count", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        span_count = min(ctx.draw_int("span_count", 2, 4), h)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)

    rows = rng.sample(range(h), span_count)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], span_count)
    for row, color in zip(rows, colors):
        gap = rng.randint(1, max(1, min(6, w - 2)))
        c0 = rng.randint(0, w - gap - 1)
        grid[row][c0] = color
        grid[row][c0 + gap] = color
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # empty grid → no spans to fill
        return g
    if name == "endpoints_adjacent":
        # endpoints touching → zero-length gap, fill is trivially empty
        g[2][3] = 4; g[2][4] = 4
        g[5][6] = 6; g[5][7] = 6
        return g
    if name == "single_endpoint":
        # only one endpoint per row → no second anchor to span to
        g[2][3] = 4
        g[5][6] = 6
        return g
    return g
