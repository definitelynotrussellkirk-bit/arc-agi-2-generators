"""Generator for arc_puzzle_bank_nineteenth21:E127.

Rule: rows contain same-color endpoints with empty horizontal spans;
fill the segment between them with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_endpoint_only, span_already_filled, no_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d48ec0001283"
VERSION = "1.1.0"
TASK_ID = "d48ec0001283"
SUMMARY = "Rows contain same-color endpoints with empty horizontal spans."

INVARIANTS = [
    "background is 0",
    "each active row has exactly two nonzero cells",
    "the two row endpoints have the same color",
    "the segment between endpoints is initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_endpoint_only", "span_already_filled", "no_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rows":           {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..9", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        target = min(ctx.draw_int("rows", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("rows", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 11)
        target = min(ctx.draw_int("rows", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    for i, r in enumerate(rows):
        left = rng.randint(0, w - 4)
        right = rng.randint(left + 2, w - 1)
        color = colors[i % len(colors)]
        g[r][left] = color
        g[r][right] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "single_endpoint_only":
        # active rows have only 1 nonzero cell → no pair, no fill
        g[1][3] = 4
        g[3][6] = 7
        return g
    if name == "span_already_filled":
        # span between endpoints is already painted → conflict with rule's fill
        g[2][1] = 5; g[2][7] = 5
        for c in range(2, 7):
            g[2][c] = 3
        return g
    if name == "no_endpoints":
        # empty grid → no rows have endpoints, rule no-op
        return g
    return g
