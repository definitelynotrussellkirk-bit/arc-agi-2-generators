"""Generator for arc_puzzle_bank_21_set5_s:S5_E2.

Rule: count blue dots → red strip of width equal to count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, dot_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dots, single_dot, dots_clustered.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "845bebcacc5c"
VERSION = "1.1.0"
TASK_ID = "845bebcacc5c"
SUMMARY = "The number of blue dots determines the width of a red strip."

INVARIANTS = [
    "background is 0",
    "all nonzero input cells are isolated blue dots",
    "the dot count is positive",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dots", "single_dot", "dots_clustered")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dot_count":      {"type": "int", "default": "rng 2..6", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(cells, r, c):
    return all(abs(r - rr) + abs(c - cc) >= 2 for rr, cc in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 8)
        count = ctx.draw_int("dot_count", 2, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("dot_count", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 10)
        count = ctx.draw_int("dot_count", 2, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = []
    for _ in range(count):
        for _attempt in range(200):
            r = rng.randrange(h)
            c = rng.randrange(w)
            if g[r][c] == 0 and _far(placed, r, c):
                g[r][c] = 1
                placed.append((r, c))
                break
        else:
            raise ValueError("could not place blue dot")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_dots":
        # zero dots → strip width 0, output is empty
        return g
    if name == "single_dot":
        # one dot → strip width 1, trivial case
        g[3][4] = 1
        return g
    if name == "dots_clustered":
        # adjacent dots → "isolated" invariant violated, could read as one blob not N dots
        for r, c in [(2, 2), (2, 3), (3, 3)]:
            g[r][c] = 1
        return g
    return g
