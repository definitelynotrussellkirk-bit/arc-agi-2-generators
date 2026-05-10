"""Generator for arc_puzzle_bank_seventeenth21:E119 — aligned same-color pair fills empty midpoint.

Rule: each unique-color endpoint pair (aligned, even span) has its
midpoint cell filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, odd_span, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e26763a6f70"
VERSION = "1.1.0"
TASK_ID = "1e26763a6f70"

SUMMARY = "Aligned same-color endpoint pairs have an empty midpoint."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the endpoints share one row or one column",
    "the endpoint span is even and midpoint cell is initially 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "odd_span", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 1..3", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("pairs", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("pairs", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pairs", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        horizontal = rng.randrange(2) == 0
        if horizontal:
            span = rng.choice([2, 4, 6][:max(1, (w - 1) // 2)])
            r = rng.randrange(h)
            c = rng.randint(0, w - span - 1)
            pts = [(r, c), (r, c + span), (r, c + span // 2)]
        else:
            span = rng.choice([2, 4, 6][:max(1, (h - 1) // 2)])
            c = rng.randrange(w)
            r = rng.randint(0, h - span - 1)
            pts = [(r, c), (r + span, c), (r + span // 2, c)]
        if any(p in reserved for p in pts):
            continue
        color = colors[placed % len(colors)]
        g[pts[0][0]][pts[0][1]] = color
        g[pts[1][0]][pts[1][1]] = color
        reserved.update(pts)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Singletons only — rule has nothing to bridge.
        g[1][1] = 3; g[3][6] = 4; g[5][2] = 5
        return g
    if name == "odd_span":
        # Endpoints aligned but span is odd — no integer midpoint.
        g[1][1] = 4; g[1][4] = 4
        g[4][2] = 6; g[4][5] = 6
        return g
    if name == "single_endpoint":
        # Each color appears once — no pair, no midpoint.
        g[1][2] = 4
        g[4][6] = 6
        return g
    return g
