"""Generator for arc_puzzle_bank_sixteenth_21_bundle:hard_109_select_shape_class_and_apply_transform_sequence.

The three-cell header selects a body shape class and two transform codes.
The body contains exactly one object with that binary class.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "72416068b0cf"
VERSION = "1.1.0"
TASK_ID = "72416068b0cf"

SUMMARY = "Header shape code plus two transform codes select and transform a matching body object."

INVARIANTS = [
    "background is 0",
    "header cells are shape-code, transform-code, transform-code",
    "the body has exactly one object matching the requested binary shape class",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 9..10", "valid": "8..12"},
    "grid_w": {"type": "int", "default": "rng 11..13", "valid": "10..15"},
    "n_distractors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
}

TARGETS = {
    1: ((0, 0), (1, 0), (2, 0), (2, 1)),
    2: ((0, 0), (0, 1), (0, 2), (1, 1)),
    3: ((0, 0), (0, 1), (1, 1), (1, 2)),
    4: ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)),
}

DISTRACTORS = [
    ((0, 0), (0, 1), (1, 0)),
    ((0, 0), (1, 0), (1, 1)),
    ((0, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 0), (0, 1), (0, 2)),
]


def _dims(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def _can_place(grid, cells, top, left):
    h = len(grid)
    w = len(grid[0])
    abs_cells = [(top + r, left + c) for r, c in cells]
    for r, c in abs_cells:
        if r < 2 or c < 0 or r >= h or c >= w:
            return False
    rs = [r for r, _ in abs_cells]
    cs = [c for _, c in abs_cells]
    for r in range(max(1, min(rs) - 1), min(h, max(rs) + 2)):
        for c in range(max(0, min(cs) - 1), min(w, max(cs) + 2)):
            if grid[r][c] != 0:
                return False
    return True


def _paint(grid, cells, top, left, color):
    for dr, dc in cells:
        grid[top + dr][left + dc] = color


def _place_random(grid, cells, rng, color):
    h = len(grid)
    w = len(grid[0])
    sh, sw = _dims(cells)
    for _ in range(200):
        top = rng.randint(2, h - sh)
        left = rng.randint(0, w - sw)
        if _can_place(grid, cells, top, left):
            _paint(grid, cells, top, left, color)
            return
    raise ValueError("could not place body object")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 9, 10)
    w = ctx.draw_int("grid_w", 11, 13)
    n_distractors = ctx.draw_int("n_distractors", 2, 3)
    rng = ctx.draw_rng("layout")

    grid = full_grid(h, w, 0)
    shape_code = rng.choice([1, 2, 3, 4])
    step1 = rng.choice([1, 2, 3, 4])
    step2 = rng.choice([1, 2, 3, 4])
    grid[0][0] = shape_code
    grid[0][1] = step1
    grid[0][2] = step2

    colors = rng.sample([5, 6, 7, 8, 9], n_distractors + 1)
    _place_random(grid, TARGETS[shape_code], rng, colors[0])

    choices = DISTRACTORS[:]
    rng.shuffle(choices)
    for cells, color in zip(choices, colors[1:]):
        _place_random(grid, cells, rng, color)

    return grid
