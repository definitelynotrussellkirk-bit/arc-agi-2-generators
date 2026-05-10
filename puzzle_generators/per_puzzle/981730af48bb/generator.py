"""Generator for arc_puzzle_bank_nineteenth21:E132 — same-color row endpoint pairs encode midpoint dots.

Rule: each row has 2 same-color endpoints with even distance; output keeps
only the midpoint dot for each pair.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: odd_distance, no_pairs, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "981730af48bb"
VERSION = "1.1.0"
TASK_ID = "981730af48bb"
SUMMARY = "Same-color row endpoint pairs encode midpoint cells."

INVARIANTS = [
    "background is 0",
    "each active row has exactly two equal-colored endpoints",
    "endpoint distance is even so the midpoint is a lattice cell",
    "the output keeps only the midpoint dots",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("odd_distance", "no_pairs", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_endpoint_pairs_even_dist",
                       "valid": "row_endpoint_pairs_even_dist"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        target = min(ctx.draw_int("pairs", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("pairs", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 11)
        target = min(ctx.draw_int("pairs", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    spans = [2, 4, 6, 8]
    for i, r in enumerate(rows):
        possible = [span for span in spans if span < w]
        span = rng.choice(possible)
        left = rng.randint(0, w - span - 1)
        color = colors[i % len(colors)]
        g[r][left] = color
        g[r][left + span] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "odd_distance":
        # endpoints with odd distance → midpoint is not a lattice cell, ill-defined
        g[1][1] = 4; g[1][4] = 4   # distance 3
        g[3][2] = 6; g[3][7] = 6   # distance 5
        return g
    if name == "no_pairs":
        # singletons only → no pair to encode
        g[1][2] = 4
        g[3][6] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints have different colors → "same-color pair" precondition fails
        g[1][1] = 4; g[1][5] = 6   # different colors
        g[3][2] = 3; g[3][6] = 7   # different colors
        return g
    return g
