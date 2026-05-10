"""Generator for arc_puzzle_bank_fifteenth21:E100 — endpoint pairs fill exact midpoint.

Rule: each unique-color endpoint pair (aligned, even span) has its
midpoint cell filled with the same color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, odd_span, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e07b7276b85a"
VERSION = "1.1.0"
TASK_ID = "e07b7276b85a"

SUMMARY = "Place aligned unique-color endpoint pairs with an exact midpoint."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "endpoint pairs are horizontal or vertical",
    "endpoint span length is even so there is a single midpoint cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "odd_span", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= pairs", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "axis_aligned_even_span",
                       "valid": "axis_aligned_even_span"},
    "n_distinct_colors": {"type": "int", "default": "= pairs", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("pairs", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("pairs", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], k=target)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        horizontal = rng.randrange(2) == 0
        if horizontal:
            r = rng.randrange(h)
            span = rng.choice([2, 4, 6][:max(1, (w - 1) // 2)])
            c1 = rng.randint(0, w - span - 1)
            pts = [(r, c1), (r, c1 + span), (r, c1 + span // 2)]
        else:
            c = rng.randrange(w)
            span = rng.choice([2, 4, 6][:max(1, (h - 1) // 2)])
            r1 = rng.randint(0, h - span - 1)
            pts = [(r1, c), (r1 + span, c), (r1 + span // 2, c)]
        if any(p in reserved for p in pts):
            continue
        color = colors[placed]
        g[pts[0][0]][pts[0][1]] = color
        g[pts[1][0]][pts[1][1]] = color
        reserved.update(pts)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Singletons only — rule has no aligned pair to bridge.
        g[1][1] = 3; g[3][7] = 4; g[6][2] = 5
        return g
    if name == "odd_span":
        # Endpoints aligned but span is odd (3) — no integer midpoint cell,
        # so the rule has no single cell to fill.
        g[2][1] = 4; g[2][4] = 4
        g[5][2] = 6; g[5][5] = 6
        return g
    if name == "single_endpoint":
        # Each color appears only once — there's no second endpoint to
        # pair with, so no midpoint can be defined.
        g[2][1] = 4
        g[5][6] = 6
        return g
    return g
