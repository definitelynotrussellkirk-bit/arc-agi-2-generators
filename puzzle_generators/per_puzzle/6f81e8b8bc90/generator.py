"""Generator for arc_puzzle_bank_21_set5_s:S5_E7.

Rule: count green dots → orange square of side equal to count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, dot_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dots, single_dot, dots_clustered.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6f81e8b8bc90"
VERSION = "1.1.0"
TASK_ID = "6f81e8b8bc90"
SUMMARY = "The number of green dots determines the side length of an orange square."

INVARIANTS = [
    "background is 0",
    "all nonzero input cells are isolated green dots",
    "the green dot count is positive",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dots", "single_dot", "dots_clustered")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dot_count":      {"type": "int", "default": "rng 2..5", "valid": "1..8"},
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
        count = ctx.draw_int("dot_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("dot_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 10)
        count = ctx.draw_int("dot_count", 2, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = []
    for _ in range(count):
        for _attempt in range(200):
            r = rng.randrange(h)
            c = rng.randrange(w)
            if g[r][c] == 0 and _far(placed, r, c):
                g[r][c] = 3
                placed.append((r, c))
                break
        else:
            raise ValueError("could not place green dot")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_dots":
        # zero dots → output is 0×0 square, ambiguous size
        return g
    if name == "single_dot":
        # one dot → output is 1×1 square, trivial case
        g[3][4] = 3
        return g
    if name == "dots_clustered":
        # adjacent dots break "isolated" invariant — could be read as one blob, not N dots
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3)]:
            g[r][c] = 3
        return g
    return g
