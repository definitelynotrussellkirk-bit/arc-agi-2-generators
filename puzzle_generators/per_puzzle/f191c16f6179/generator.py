"""Generator for arc_puzzle_bank_fifth21:E29.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, axis_aligned, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f191c16f6179"
VERSION = "1.1.0"
TASK_ID = "f191c16f6179"

SUMMARY = "Place matching diagonal endpoint pairs with empty 45-degree gaps."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "same-color cells are separated diagonal endpoints",
    "interior diagonal cells are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "diagonal_endpoint_pairs",
                       "valid": "diagonal_endpoint_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _diag(a, b):
    r0, c0 = a
    r1, c1 = b
    sr = 1 if r1 > r0 else -1
    sc = 1 if c1 > c0 else -1
    return [(r0 + sr * k, c0 + sc * k) for k in range(abs(r1 - r0) + 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], k=target)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        length = rng.randint(2, min(5, h - 1, w - 1))
        r0 = rng.randint(0, h - length - 1)
        c0 = rng.randint(0, w - length - 1)
        if rng.randrange(2):
            a, b = (r0, c0), (r0 + length, c0 + length)
        else:
            a, b = (r0, c0 + length), (r0 + length, c0)
        cells = _diag(a, b)
        if any(p in reserved for p in cells):
            continue
        color = colors[placed]
        g[a[0]][a[1]] = color
        g[b[0]][b[1]] = color
        reserved.update(cells)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal endpoints
        return g
    if name == "axis_aligned":
        # endpoints align horizontally/vertically (not diagonal)
        g[3][1] = 4; g[3][7] = 4
        g[1][5] = 6; g[6][5] = 6
        return g
    if name == "single_endpoint":
        # only 1 cell per color → no pair
        g[2][2] = 4
        g[5][7] = 6
        return g
    return g
