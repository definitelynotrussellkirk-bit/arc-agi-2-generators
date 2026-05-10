"""Generator for arc_puzzle_bank_21_set3:S3_H7.

The top row is a size-to-color legend.  Gray objects in the body are recolored
according to the legend entry matching each object's cell count.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a7e26e20850c"
VERSION = "1.1.0"
TASK_ID = "a7e26e20850c"

SUMMARY = "Top-row run lengths map gray object sizes to recolor targets."

INVARIANTS = [
    "background is 0",
    "top row contains separated nonzero color runs",
    "each gray body object has a size present in the top-row legend",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 9..11", "valid": "7..13"},
    "grid_w": {"type": "int", "default": "rng 14..16", "valid": "12..18"},
    "n_sizes": {"type": "int", "default": "rng 3..4", "valid": "2..4"},
}

SHAPES = {
    2: [
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
    ],
    3: [
        ((0, 0), (1, 0), (1, 1)),
        ((0, 0), (0, 1), (0, 2)),
        ((0, 0), (1, 0), (2, 0)),
    ],
    4: [
        ((0, 0), (0, 1), (1, 0), (1, 1)),
        ((0, 0), (1, 0), (2, 0), (2, 1)),
    ],
    5: [
        ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
        ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ],
}


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


def _place_object(grid, cells, rng):
    h = len(grid)
    w = len(grid[0])
    sh, sw = _dims(cells)
    for _ in range(200):
        top = rng.randint(2, h - sh)
        left = rng.randint(0, w - sw)
        if _can_place(grid, cells, top, left):
            _paint(grid, cells, top, left, 5)
            return
    raise ValueError("could not place gray object")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 9, 11)
    w = ctx.draw_int("grid_w", 14, 16)
    n_sizes = ctx.draw_int("n_sizes", 3, 4)
    rng = ctx.draw_rng("layout")

    sizes = rng.sample([2, 3, 4, 5], n_sizes)
    colors = rng.sample([2, 3, 4, 6, 7, 8, 9], n_sizes)

    grid = full_grid(h, w, 0)
    c = rng.randint(0, 1)
    for size, color in zip(sizes, colors):
        if c + size > w:
            raise ValueError("legend does not fit")
        for dc in range(size):
            grid[0][c + dc] = color
        c += size + rng.randint(1, 2)

    object_sizes = sizes[:]
    if n_sizes == 3:
        object_sizes.append(rng.choice(sizes))
    rng.shuffle(object_sizes)
    for size in object_sizes:
        _place_object(grid, rng.choice(SHAPES[size]), rng)

    return grid
