"""Generator for arc_puzzle_bank_tenth_21_bundle:easy_64_fill_between_matching_endpoints.

Rule: rows contain matching same-color endpoints whose span is filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_endpoint_only, span_already_filled, no_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2038a3a66886"
VERSION = "1.1.0"
TASK_ID = "2038a3a66886"
SUMMARY = "Rows contain matching same-color endpoints whose span is filled."

INVARIANTS = [
    "background is 0",
    "each active row has one same-color endpoint pair",
    "interior cells between endpoints are empty",
    "rows are processed independently",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_endpoint_only", "span_already_filled", "no_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rows":           {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..9", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 11)
        target = min(ctx.draw_int("rows", 3, 4), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        target = min(ctx.draw_int("rows", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        target = min(ctx.draw_int("rows", 3, 5), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), target):
        c0 = rng.randint(0, w - 3)
        c1 = rng.randint(c0 + 2, w - 1)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[r][c0] = color
        g[r][c1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "single_endpoint_only":
        # active rows have just one endpoint → no pair, rule is no-op
        g[1][3] = 4
        g[3][6] = 7
        return g
    if name == "span_already_filled":
        # span between endpoints is already painted with another color → conflict
        g[2][1] = 5; g[2][8] = 5
        for c in range(2, 8):
            g[2][c] = 3
        return g
    if name == "no_endpoints":
        # empty grid → nothing to fill
        return g
    return g
