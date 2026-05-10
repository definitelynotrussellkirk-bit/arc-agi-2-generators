"""Generator for arc_puzzle_bank_21_set18_s:S18_E4.

Rule: each active row contains 2 endpoints; the output paints only the
bridge cells strictly between them (endpoints themselves are dropped).

Combinatorial axes (8): grid_h/w, palette_kind, active_rows, gap_min,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: endpoints_adjacent, single_endpoint, three_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a0076c1c960c"
VERSION = "1.1.0"
TASK_ID = "a0076c1c960c"
SUMMARY = "Horizontal row endpoints produce only the bridge cells between them."

INVARIANTS = [
    "active rows contain two endpoints with at least one gap cell between them",
    "output omits the original endpoints",
    "only bridge cells are painted",
]

PALETTE_KINDS = ("default", "wide_gap", "tight_gap", "rainbow")
DEGENERATE_TEXTURES = ("endpoints_adjacent", "single_endpoint", "three_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "width":          {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 2..3",
                       "valid": "1..height"},
    "gap_min":        {"type": "int", "default": "1", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3",
                          "valid": "2..3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 6, 7)
        w = ctx.draw_int("width", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 9, 10)
    else:
        h = ctx.draw_int("height", 6, 8)
        w = ctx.draw_int("width", 7, 10)
    n = ctx.draw_int("active_rows", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for idx, r in enumerate(rng.sample(range(h), n)):
        c1 = rng.randint(0, w - 5)
        c2 = rng.randint(c1 + 3, w - 1)
        g[r][c1] = 2 + idx
        g[r][c2] = 2 + idx
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "endpoints_adjacent":
        # endpoints touch — no gap cell, output is empty
        g[2][3] = 2
        g[2][4] = 2
        g[5][1] = 3
        g[5][2] = 3
        return g
    if name == "single_endpoint":
        # only one endpoint — no pair to bridge
        g[2][3] = 2
        g[5][6] = 3
        return g
    if name == "three_endpoints":
        # 3 endpoints in same row — bridge selection ambiguous
        g[3][1] = 4
        g[3][4] = 4
        g[3][7] = 4
        return g
    return g
