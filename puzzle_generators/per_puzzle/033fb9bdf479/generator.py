"""Generator for arc_puzzle_bank_21_set4:S4_H3.

Magenta markers encode a hole count. Among the green objects, exactly
one object has that many enclosed holes and should be recolored.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "033fb9bdf479"
VERSION = "1.1.0"
TASK_ID = "033fb9bdf479"

SUMMARY = "Magenta marker count selects the green object with matching hole count."

INVARIANTS = [
    "background is 0",
    "marker color is 6",
    "candidate objects are green 3",
    "exactly one green object has the marker-specified number of holes",
]

AXES = {
    "height": {"type": "int", "default": "rng 10..12", "valid": "9..13"},
    "width": {"type": "int", "default": "rng 15..17", "valid": "13..18"},
    "hole_count": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
}

ONE_HOLE = [
    (0, 0), (0, 1), (0, 2),
    (1, 0),         (1, 2),
    (2, 0), (2, 1), (2, 2),
]

TWO_HOLES = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 0),         (1, 2),         (1, 4),
    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
]

SOLID = [(0, 0), (0, 1), (1, 0), (1, 1)]


def _paint(g, top, left, cells, color=3):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("height", 10, 12)
    w = ctx.draw_int("width", 15, 17)
    hole_count = ctx.draw_int("hole_count", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    for c in range(hole_count):
        g[0][c] = 6

    row = rng.randint(3, min(5, h - 5))
    if hole_count == 1:
        _paint(g, row, 1, ONE_HOLE)
        _paint(g, row, 6, TWO_HOLES)
        _paint(g, h - 3, w - 4, SOLID)
    else:
        _paint(g, row, 1, ONE_HOLE)
        _paint(g, row, 6, TWO_HOLES)
        _paint(g, h - 3, w - 4, SOLID)
    return g
