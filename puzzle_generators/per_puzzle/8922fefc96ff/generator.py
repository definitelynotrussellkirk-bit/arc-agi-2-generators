"""Generator for arc_puzzle_bank_21_set2:S2_E3.

Rule: rows with exactly two orange endpoints and an empty gap are
filled horizontally between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, span_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_endpoint_only, span_already_filled, no_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8922fefc96ff"
VERSION = "1.1.0"
TASK_ID = "8922fefc96ff"
SUMMARY = "Rows with exactly two orange endpoints and an empty gap are filled horizontally."

INVARIANTS = [
    "background is 0",
    "active rows have exactly two orange cells",
    "the span between each endpoint pair starts empty",
    "rows with one orange cell remain unchanged",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_endpoint_only", "span_already_filled", "no_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "span_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("span_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        count = ctx.draw_int("span_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 12)
        count = ctx.draw_int("span_count", 2, min(4, h))
    count = min(count, h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), count)
    for r in rows:
        c1 = rng.randint(0, w - 4)
        c2 = rng.randint(c1 + 2, w - 1)
        g[r][c1] = 7
        g[r][c2] = 7
    inactive = [r for r in range(h) if r not in rows]
    if inactive:
        g[rng.choice(inactive)][rng.randrange(w)] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "single_endpoint_only":
        # every active row has just one orange cell → no pair, rule is no-op
        for r in range(h):
            g[r][rng_pick(r, w) if False else (r * 2 % w)] = 7
        return g
    if name == "span_already_filled":
        # span between endpoints is already painted with another color → conflict
        g[1][1] = 7; g[1][7] = 7
        for c in range(2, 7):
            g[1][c] = 4
        return g
    if name == "no_endpoints":
        # no orange cells at all → nothing to fill
        for r, c in [(2, 3), (4, 6)]:
            g[r][c] = 5
        return g
    return g
