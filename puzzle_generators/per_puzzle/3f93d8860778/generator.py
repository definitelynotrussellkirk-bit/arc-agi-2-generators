"""Generator for arc_puzzle_bank_eighteenth_21_bundle:easy_122_fill_vertical_spans_between_matching_endpoints.

Rule: fill vertical intervals between matching column endpoints.

Combinatorial axes (8): grid_h, grid_w, palette_kind, spans,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, mismatched_endpoints, span_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3f93d8860778"
VERSION = "1.1.0"
TASK_ID = "3f93d8860778"
SUMMARY = "Fill vertical intervals between matching column endpoints."

INVARIANTS = [
    "background is 0",
    "active columns contain exactly two same-color endpoints",
    "endpoint pairs are separated by at least one zero",
    "output fills the inclusive column interval",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "mismatched_endpoints", "span_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "spans":          {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "col_endpoint_pairs",
                       "valid": "col_endpoint_pairs"},
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
        n = min(ctx.draw_int("spans", 3, 3), w, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 9, 10)
        n = min(ctx.draw_int("spans", 4, 5), w, 9)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 10)
        n = min(ctx.draw_int("spans", 3, 5), w, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for c, color in zip(cols, colors):
        r1 = rng.randint(0, h - 3)
        r2 = rng.randint(r1 + 2, h - 1)
        g[r1][c] = color
        g[r2][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only → no pair to fill span between
        g[2][1] = 4
        g[6][3] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints with different colors → "same-color pair" precondition fails
        g[1][1] = 4; g[6][1] = 6   # mismatched (different colors in same col)
        g[2][3] = 3; g[7][3] = 7
        return g
    if name == "span_already_filled":
        # span already non-zero → no empty cells to fill
        for r in range(1, 7): g[r][1] = 4   # full column
        g[1][3] = 6; g[3][3] = 9; g[5][3] = 6   # midpoint non-zero
        return g
    return g
