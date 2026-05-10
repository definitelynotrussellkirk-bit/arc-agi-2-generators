"""Generator for arc_puzzle_bank_21_set8_s:S8_M3.

The cyan bar is the fold axis.  Nonzero cells on the left are compared to
their reflected right-half partners; mismatched occupancy becomes orange.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9a1459fe40d0"
VERSION = "1.1.0"
TASK_ID = "9a1459fe40d0"

SUMMARY = "Fold the left half across a cyan bar and mark occupancy XOR on the right."

INVARIANTS = [
    "background is 0",
    "a full vertical color-8 bar separates equal-width halves",
    "nonzero cells appear on both sides of the bar",
    "at least one mirrored pair has exactly one occupied cell",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "half_w": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "density": {"type": "float", "default": "rng sparse xor pairs", "valid": "0.2..0.7"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 7, 9)
    half_w = ctx.draw_int("half_w", 4, 6)
    w = half_w * 2 + 1
    bar_c = half_w
    rng = ctx.draw_rng("layout")

    grid = full_grid(h, w, 0)
    for r in range(h):
        grid[r][bar_c] = 8

    colors = [1, 2, 3, 4, 5, 6, 7, 9]
    pairs = [(r, c) for r in range(1, h - 1) for c in range(0, half_w)]
    rng.shuffle(pairs)

    pair_count = rng.randint(max(5, len(pairs) // 4), max(6, len(pairs) // 2))
    selected = pairs[:pair_count]
    xor_slots = set(rng.sample(range(pair_count), rng.randint(2, max(2, pair_count // 2))))

    for idx, (r, c) in enumerate(selected):
        mc = 2 * bar_c - c
        color_left = rng.choice(colors)
        color_right = rng.choice(colors)
        if idx in xor_slots:
            if rng.choice([True, False]):
                grid[r][c] = color_left
            else:
                grid[r][mc] = color_right
        else:
            if rng.choice([True, False]):
                grid[r][c] = color_left
                grid[r][mc] = color_right

    return grid
