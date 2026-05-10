"""Generator for arc_puzzle_bank_21_set5_s:S5_E6.

Rule: rows with exactly two blue endpoints are filled into horizontal
segments.

Combinatorial axes (8): grid_h, grid_w, palette_kind, segment_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_endpoint_only, span_already_filled, no_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6af5c333e5c1"
VERSION = "1.1.0"
TASK_ID = "6af5c333e5c1"
SUMMARY = "Rows with exactly two blue endpoints are filled into horizontal segments."

INVARIANTS = [
    "background is 0",
    "active rows contain exactly two blue cells",
    "optional inactive rows contain one blue cell",
    "all cells between the endpoints start empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_endpoint_only", "span_already_filled", "no_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "segment_count":  {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 10)
        count = ctx.draw_int("segment_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        count = ctx.draw_int("segment_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        count = ctx.draw_int("segment_count", 2, min(4, h))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), count)
    for r in rows:
        c1 = rng.randint(0, w - 4)
        c2 = rng.randint(c1 + 2, w - 1)
        g[r][c1] = 1
        g[r][c2] = 1
    inactive = [r for r in range(h) if r not in rows]
    if inactive:
        r = rng.choice(inactive)
        g[r][rng.randrange(w)] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "single_endpoint_only":
        # every row has just one blue cell → rule's "two endpoints" filter never matches
        for r in range(h):
            g[r][r % w] = 1
        return g
    if name == "span_already_filled":
        # span between the two blue endpoints is already painted with another color → conflict
        g[2][1] = 1; g[2][7] = 1
        for c in range(2, 7):
            g[2][c] = 4
        return g
    if name == "no_endpoints":
        # empty grid → no rows have endpoints, rule is no-op
        return g
    return g
