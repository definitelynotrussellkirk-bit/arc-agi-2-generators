"""Generator for arc_puzzle_bank_sixth_21_bundle:easy_40_fill_between_vertical_markers.

Rule: same-color vertical marker pairs fill their column segment.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, single_endpoint_per_col, endpoints_adjacent.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2ab8c1aaa3e2"
VERSION = "1.1.0"
TASK_ID = "2ab8c1aaa3e2"
SUMMARY = "Same-color vertical marker pairs fill their column segment."

INVARIANTS = [
    "background is 0",
    "each active column has a color appearing exactly twice",
    "the two matching cells mark the vertical segment endpoints",
    "other colors do not form extra pairs in that column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint_per_col", "endpoints_adjacent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "column_pairs",
                       "valid": "column_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        target = min(ctx.draw_int("pairs", 3, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("pairs", 4, 5), w)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 11)
        target = min(ctx.draw_int("pairs", 3, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), target)
    for c in cols:
        r0 = rng.randint(0, h - 3)
        r1 = rng.randint(r0 + 2, h - 1)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[r0][c] = color
        g[r1][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 9
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # empty grid → nothing to fill between
        return g
    if name == "single_endpoint_per_col":
        # one marker per column → no second endpoint to span to
        g[3][2] = 4
        g[5][5] = 6
        return g
    if name == "endpoints_adjacent":
        # endpoints touching → no gap to fill
        g[2][3] = 4; g[3][3] = 4
        g[5][6] = 6; g[6][6] = 6
        return g
    return g
