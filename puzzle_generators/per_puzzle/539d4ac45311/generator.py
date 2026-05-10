"""Generator for arc_puzzle_bank_21_set19_bundle:easy_p01.

Rule: rows contain two same-color endpoints with an empty span between
them; output draws the connecting line filling the span.

Combinatorial axes (8): grid_h, grid_w, palette_kind, span_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, span_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "539d4ac45311"
VERSION = "1.1.0"
TASK_ID = "539d4ac45311"
SUMMARY = "Rows contain two same-color endpoints with an empty span between them."

INVARIANTS = [
    "background is 0",
    "each active row has exactly two nonzero cells",
    "the two cells in an active row share one color and have only zeros between them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "span_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "span_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_endpoint_pairs",
                       "valid": "row_endpoint_pairs"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        span_count = min(ctx.draw_int("span_count", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        span_count = min(ctx.draw_int("span_count", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 8, 12)
        span_count = min(ctx.draw_int("span_count", 2, 4), h)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)

    rows = rng.sample(range(h), span_count)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], span_count)
    for row, color in zip(rows, colors):
        gap = rng.randint(1, max(1, min(5, w - 2)))
        c1 = rng.randint(0, w - gap - 1)
        c2 = c1 + gap
        grid[row][c1] = color
        grid[row][c2] = color
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons in rows → no endpoints to bridge
        g[1][2] = 4
        g[3][5] = 6
        return g
    if name == "span_already_filled":
        # span between endpoints already has nonzero cells → rule's "empty span" precondition fails
        g[1][1] = 4; g[1][2] = 4; g[1][3] = 4; g[1][4] = 4   # no gap, all filled
        g[3][1] = 6; g[3][3] = 9; g[3][5] = 6                # midpoint has different color
        return g
    if name == "mismatched_endpoints":
        # endpoints with different colors → "same-color pair" rule precondition fails
        g[1][1] = 4; g[1][6] = 6   # mismatched
        g[3][2] = 3; g[3][7] = 7   # mismatched
        return g
    return g
