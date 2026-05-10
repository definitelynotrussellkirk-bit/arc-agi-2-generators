"""Generator for arc_puzzle_bank_fifteenth_21_bundle:easy_100_fill_antidiagonal_spans.

Place same-color pairs on slope -1 diagonals, leaving the span empty.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, length_1_pair, main_diagonal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d57b7deebba2"
VERSION = "1.1.0"
TASK_ID = "d57b7deebba2"

SUMMARY = "Place same-color pairs on slope -1 diagonals, leaving the span empty."

INVARIANTS = [
    "background is 0",
    "same-color cells share an anti-diagonal line",
    "the anti-diagonal span between them is initially empty",
    "anti-diagonal spans do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "length_1_pair", "main_diagonal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "anti_diagonal_pairs",
                       "valid": "anti_diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
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
        c0 = rng.randint(length, w - 1)
        cells = [(r0 + k, c0 - k) for k in range(length + 1)]
        if any(p in reserved for p in cells):
            continue
        color = colors[placed]
        g[r0][c0] = color
        g[r0 + length][c0 - length] = color
        reserved.update(cells)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no anti-diagonal pairs to span-fill
        return g
    if name == "length_1_pair":
        # adjacent anti-diagonal cells → no empty span between them
        g[2][6] = 4; g[3][5] = 4
        return g
    if name == "main_diagonal":
        # main diagonal pair (slope +1) → not slope -1, rule won't fire
        g[2][2] = 4; g[5][5] = 4
        return g
    return g
