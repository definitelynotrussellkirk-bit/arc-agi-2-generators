"""Generator for arc_puzzle_bank_fifth_21_bundle:easy_32_fill_between_row_endpoints.

Rule: rows with two same-color endpoints have the cells between them filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_spans,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, mismatched_endpoints, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ffa91bb651d1"
VERSION = "1.1.0"
TASK_ID = "ffa91bb651d1"
SUMMARY = "Rows with two matching endpoint cells are filled across."

INVARIANTS = [
    "background is 0",
    "target rows have exactly two nonzero cells",
    "the two target cells share a color",
    "some rows may contain distractor non-matching endpoints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "mismatched_endpoints", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_spans":        {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        n_spans = ctx.draw_int("n_spans", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n_spans = ctx.draw_int("n_spans", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        n_spans = ctx.draw_int("n_spans", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), min(n_spans, h))
    for i, r in enumerate(rows):
        c1 = rng.randint(0, w - 4)
        c2 = rng.randint(c1 + 2, w - 1)
        g[r][c1] = colors[i % len(colors)]
        g[r][c2] = colors[i % len(colors)]
    if h > len(rows):
        r = next(rr for rr in range(h) if rr not in rows)
        g[r][1] = colors[0]
        g[r][w - 2] = colors[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # blank → no spans to fill, rule has no effect
        return g
    if name == "mismatched_endpoints":
        # all rows have two endpoints but in different colors → rule's predicate fails everywhere
        g[1][1] = 4; g[1][w - 2] = 6
        g[3][2] = 3; g[3][w - 1] = 8
        g[5][0] = 7; g[5][5] = 4
        return g
    if name == "single_endpoint":
        # rows have only one endpoint each → no pair, rule has no effect
        g[1][3] = 4
        g[3][5] = 6
        g[5][7] = 3
        return g
    return g
