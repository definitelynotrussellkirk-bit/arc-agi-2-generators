"""Generator for arc_puzzle_bank_21_set18_s:S18_E1.

Rule: sparse row endpoints expand to filled horizontal spans.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_endpoint_only, span_already_filled, no_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "89dfcff52ee8"
VERSION = "1.1.0"
TASK_ID = "89dfcff52ee8"
SUMMARY = "Sparse row endpoints expand to filled horizontal spans."

INVARIANTS = [
    "nonzero cells appear on two or three rows",
    "each active row has at least two endpoints",
    "the output fills every cell between each row's extreme endpoints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_endpoint_only", "span_already_filled", "no_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 2..3", "valid": "1..height"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..6"},
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
        h = ctx.draw_int("height", 6, 6)
        w = ctx.draw_int("width", 7, 8)
        n = ctx.draw_int("active_rows", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 9, 10)
        n = ctx.draw_int("active_rows", 3, 3)
    else:
        h = ctx.draw_int("height", 6, 8)
        w = ctx.draw_int("width", 7, 10)
        n = ctx.draw_int("active_rows", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), n)
    colors = [2, 3, 4, 5, 6, 7]
    for idx, r in enumerate(rows):
        c1 = rng.randint(0, w - 5)
        c2 = rng.randint(c1 + 3, w - 1)
        g[r][c1] = colors[idx]
        g[r][c2] = colors[idx]
        if rng.random() < 0.5:
            g[r][rng.randint(c1 + 1, c2 - 1)] = colors[idx]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "single_endpoint_only":
        # active rows have only 1 endpoint → no span to expand
        g[1][3] = 4
        g[3][6] = 6
        return g
    if name == "span_already_filled":
        # span between extremes is already painted with another color → conflict
        g[2][1] = 5; g[2][7] = 5
        for c in range(2, 7):
            g[2][c] = 3
        return g
    if name == "no_endpoints":
        # empty grid → no rows have endpoints
        return g
    return g
