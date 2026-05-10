"""Generator for arc_puzzle_bank_21_set18_s:S18_E2.

Rule: each active column's extreme nonzero endpoints expand to fill
every cell between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, single_endpoint_per_col, already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2fd7d58a066c"
VERSION = "1.1.0"
TASK_ID = "2fd7d58a066c"
SUMMARY = "2-3 active columns each with two distant endpoints in distinct colors."

INVARIANTS = [
    "background is 0",
    "nonzero cells appear on two or three columns",
    "each active column has at least two endpoints",
    "the output fills every cell between each column's extreme endpoints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint_per_col", "already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_cols":    {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "vertical_columns",
                       "valid": "vertical_columns"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
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
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 6, 7)
        n = ctx.draw_int("active_cols", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 7, 8)
        n = ctx.draw_int("active_cols", 3, 3)
    else:
        h = ctx.draw_int("height", 7, 10)
        w = ctx.draw_int("width", 6, 8)
        n = ctx.draw_int("active_cols", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n)
    colors = [2, 3, 4, 5, 6, 7]
    for idx, c in enumerate(cols):
        r1 = rng.randint(0, h - 5)
        r2 = rng.randint(r1 + 3, h - 1)
        g[r1][c] = colors[idx]
        g[r2][c] = colors[idx]
        if rng.random() < 0.5:
            g[rng.randint(r1 + 1, r2 - 1)][c] = colors[idx]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 7
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # empty grid → rule has nothing to expand
        return g
    if name == "single_endpoint_per_col":
        # one cell per active column → no second endpoint to anchor the span
        g[2][2] = 3
        g[5][4] = 5
        return g
    if name == "already_filled":
        # full vertical span already painted → rule is identity
        for r in range(1, 6):
            g[r][2] = 3
        for r in range(2, 7):
            g[r][4] = 5
        return g
    return g
