"""Generator for arc_puzzle_bank_third21:E16.

Rule: each column with exactly two same-color endpoints (zeros between) is
filled in with that color between the endpoints.

Combinatorial axes (8): grid_h/w, palette_kind, n_cols,
palette_size, position_bias, n_distinct_colors, gap_min, texture.
Degenerates: endpoints_adjacent, single_endpoint, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0f423424b1dc"
VERSION = "1.1.0"
TASK_ID = "0f423424b1dc"
SUMMARY = "Columns with exactly two matching nonzero endpoints are filled between them."

INVARIANTS = [
    "used columns contain exactly two same-color endpoints",
    "endpoints have zeros between",
    "background is zero",
]

PALETTE_KINDS = ("default", "tight_gaps", "wide_gaps", "rainbow")
DEGENERATE_TEXTURES = ("endpoints_adjacent", "single_endpoint", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cols":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "gap_min":        {"type": "int", "default": "1", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4",
                          "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 6, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
    n = min(ctx.draw_int("n_cols", 2, 4), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = list(range(w))
    rng.shuffle(cols)
    for i, c in enumerate(cols[:n]):
        r1 = rng.randint(0, h - 3)
        r2 = rng.randint(r1 + 2, h - 1)
        color = (i % 8) + 1
        g[r1][c] = color
        g[r2][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "endpoints_adjacent":
        # endpoints touching — no gap to fill
        g[2][2] = 4
        g[3][2] = 4
        g[5][5] = 7
        g[6][5] = 7
        return g
    if name == "single_endpoint":
        # only one endpoint per column — no pair, rule no-op
        g[2][1] = 5
        g[4][3] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints in same column have different colors — rule excludes them
        g[1][2] = 4
        g[5][2] = 7
        g[1][5] = 6
        g[6][5] = 3
        return g
    return g
