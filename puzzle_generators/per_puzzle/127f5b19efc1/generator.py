"""Generator for arc_puzzle_bank_fifth_21_bundle:hard_30_assemble_transform_panel.

The bottom row lists four transform keys.  The largest nonzero object above the
keys is the template that the canonical rule turns into a 2x2 panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "127f5b19efc1"
VERSION = "1.1.0"
TASK_ID = "127f5b19efc1"

SUMMARY = "A main template object plus bottom-row keys 1-4 that request transforms."

INVARIANTS = [
    "background is 0",
    "exactly four bottom-row key cells use colors 1, 2, 3, and 4",
    "one connected template object above the key row is larger than any key singleton",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w": {"type": "int", "default": "rng 11..14", "valid": "10..16"},
}

SHAPES = [
    ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (1, 1), (1, 2), (2, 2)),
    ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 0), (2, 0)),
    ((0, 2), (1, 0), (1, 1), (1, 2), (2, 2)),
]


def _normalized(cells):
    materialized = tuple(cells)
    r0 = min(r for r, _ in materialized)
    c0 = min(c for _, c in materialized)
    return tuple(sorted((r - r0, c - c0) for r, c in materialized))


def _turn_once(cells):
    return _normalized((c, -r) for r, c in cells)


def _oriented(cells, turns):
    out = tuple(cells)
    for _ in range(turns % 4):
        out = _turn_once(out)
    return out


def _dims(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 8, 10)
    w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")

    grid = full_grid(h, w, 0)
    shape = _oriented(rng.choice(SHAPES), rng.randint(0, 3))
    sh, sw = _dims(shape)
    top = rng.randint(1, h - sh - 3)
    left = rng.randint(1, w - sw - 1)
    color = rng.choice([5, 6, 7, 8, 9])
    for dr, dc in shape:
        grid[top + dr][left + dc] = color

    keys = [1, 2, 3, 4]
    rng.shuffle(keys)
    start = rng.randint(0, w - 7)
    for i, key in enumerate(keys):
        grid[h - 1][start + i * 2] = key

    return grid
