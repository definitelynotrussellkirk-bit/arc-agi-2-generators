"""Generator for arc_puzzle_bank_21_set13_bundle:easy_m02 — diagonal pair midpoint fill.

Same-color cells occupy opposite corners of length-3 diagonals. The
midpoint is zero and is filled with that color by the rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pair_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, axis_aligned, midpoint_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d19732b92d4a"
VERSION = "1.1.0"
TASK_ID = "d19732b92d4a"
SUMMARY = "Separated opposite-corner diagonal pairs with zero centers."

INVARIANTS = [
    "background is 0",
    "each color marks exactly one length-3 diagonal pair",
    "pair midpoint is zero",
    "diagonal neighborhoods are separated to avoid accidental bridges",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "midpoint_blocked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pair_count":     {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "= pair_count", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_pairs",
                       "valid": "scattered_diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= pair_count", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_neighborhood(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 1), min(h, r + 2)):
        for cc in range(max(0, c - 1), min(w, c + 2)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        pair_count = ctx.draw_int("pair_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
        pair_count = ctx.draw_int("pair_count", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        pair_count = ctx.draw_int("pair_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=pair_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    placed = 0
    for color in colors:
        for _ in range(250):
            r = rng.randint(1, h - 2)
            c = rng.randint(1, w - 2)
            dr, dc = rng.choice([(1, 1), (1, -1)])
            a = (r - dr, c - dc)
            b = (r + dr, c + dc)
            if _clear_neighborhood(g, r, c):
                g[a[0]][a[1]] = color
                g[b[0]][b[1]] = color
                placed += 1
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Singletons only — no diagonal pair to bridge.
        g[1][1] = 3; g[3][6] = 4; g[6][2] = 5
        return g
    if name == "axis_aligned":
        # Same-color pairs but on the same row/column (axis-aligned, not
        # diagonal) — rule's diagonal-pair filter doesn't match.
        g[2][1] = 3; g[2][5] = 3
        g[5][3] = 5; g[5][7] = 5
        return g
    if name == "midpoint_blocked":
        # Diagonal pair correctly placed, but the midpoint is already
        # non-zero (different color) — rule cannot fill it cleanly.
        g[1][1] = 4; g[3][3] = 4; g[2][2] = 7
        g[4][6] = 6; g[6][4] = 6; g[5][5] = 8
        return g
    return g
