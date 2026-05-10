"""Generator for arc_puzzle_bank_thirteenth21:E88 — equal endpoints two cells apart fill midpoint.

Rule: each pair of equal-color endpoints, two cells apart in a row or
column, has its zero midpoint filled with the same color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, not_aligned, midpoint_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fe54bfae4cee"
VERSION = "1.1.0"
TASK_ID = "fe54bfae4cee"

SUMMARY = "Equal endpoints two cells apart fill their straight midpoint."

INVARIANTS = [
    "background is 0",
    "each target pair is horizontal or vertical with one zero midpoint",
    "target colors are unique per pair",
    "pairs are spaced to avoid unintended midpoint matches",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "not_aligned", "midpoint_blocked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "= pairs", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "axis_aligned_pairs",
                       "valid": "axis_aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= pairs", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_neighborhood(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("pairs", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("pairs", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(9, target))
    placed = 0
    for _ in range(120):
        if placed >= target:
            break
        vertical = rng.choice([False, True])
        if vertical:
            r, c = rng.randint(0, h - 3), rng.randrange(w)
            cells = [(r, c), (r + 2, c)]
        else:
            r, c = rng.randrange(h), rng.randint(0, w - 3)
            cells = [(r, c), (r, c + 2)]
        if _clear_neighborhood(g, cells):
            color = colors[placed % len(colors)]
            for rr, cc in cells:
                g[rr][cc] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Singletons only — no pair to bridge.
        g[1][1] = 3; g[3][5] = 4; g[6][2] = 5
        return g
    if name == "not_aligned":
        # Equal-color pairs but they're diagonal (not row/col aligned) —
        # rule's straight-midpoint criterion never matches.
        g[1][1] = 3; g[3][3] = 3
        g[2][6] = 4; g[5][3] = 4
        return g
    if name == "midpoint_blocked":
        # Endpoints aligned + 2 cells apart but the midpoint is already
        # non-zero (a different color), so the rule can't fill it cleanly.
        g[2][1] = 3; g[2][3] = 3; g[2][2] = 7
        g[5][2] = 5; g[5][4] = 5; g[5][3] = 8
        return g
    return g
