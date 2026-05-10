"""Generator for arc_puzzle_bank_21_set13_bundle:hard_m02.

Builds a top-row transform script and a single colored template object.
The rule applies each script code cumulatively and packs the resulting
states as a left-to-right gallery.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ce3c0854174d"
VERSION = "1.1.0"
TASK_ID = "ce3c0854174d"

SUMMARY = "A top-row script controls repeated transforms of one template object."

INVARIANTS = [
    "background is 0",
    "row 0 contains only transform codes 1..4 followed by zeros",
    "exactly one connected template object appears below row 0",
]

AXES = {
    "height": {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "width": {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "script_len": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
}

SHAPES = [
    [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
]


def _dims(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def _paint(g, cells, top, left, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("height", 8, 10)
    w = ctx.draw_int("width", 11, 14)
    script_len = ctx.draw_int("script_len", 3, 4)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    script = [rng.choice([1, 2, 3, 4]) for _ in range(script_len)]
    for c, code in enumerate(script):
        g[0][c] = code

    shape = rng.choice(SHAPES)
    sh, sw = _dims(shape)
    top = rng.randint(2, h - sh - 1)
    left = rng.randint(script_len + 1, w - sw - 1)
    color = rng.choice([5, 6, 7, 8, 9])
    _paint(g, shape, top, left, color)
    return g
