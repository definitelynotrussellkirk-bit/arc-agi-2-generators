"""Generator for v2_meta_puzzles:H2.

Markers 1 and 2 define a displacement vector.  The color-3 object is copied by
that vector and rendered in color 2 by the canonical rule.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "83e2dcfca651"
VERSION = "1.1.0"
TASK_ID = "83e2dcfca651"

SUMMARY = "Translate a color-3 object by the vector from marker 1 to marker 2."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 marker and one color-2 marker define a nonzero vector",
    "one connected color-3 object has an in-bounds translated copy",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 8..10", "valid": "6..12"},
    "grid_w": {"type": "int", "default": "rng 10..13", "valid": "8..15"},
}

SHAPES = [
    ((0, 0), (0, 1), (0, 2), (1, 1)),
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((0, 0), (0, 1), (1, 0), (2, 0)),
    ((0, 1), (1, 0), (1, 1), (1, 2)),
    ((0, 0), (0, 1), (1, 1)),
]

VECTORS = [
    (-3, 1), (-2, -2), (-2, 3), (-1, -3), (-1, 2),
    (1, -2), (1, 3), (2, -3), (2, 2), (3, -1),
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


def _absolute(cells, r0, c0):
    return {(r0 + r, c0 + c) for r, c in cells}


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
    w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")

    for _ in range(300):
        dr, dc = rng.choice(VECTORS)
        shape = _oriented(rng.choice(SHAPES), rng.randint(0, 3))
        sh, sw = _dims(shape)

        min_r = max(0, -dr)
        max_r = min(h - sh, h - sh - dr)
        min_c = max(0, -dc)
        max_c = min(w - sw, w - sw - dc)
        if min_r > max_r or min_c > max_c:
            continue

        r0 = rng.randint(min_r, max_r)
        c0 = rng.randint(min_c, max_c)
        source_cells = _absolute(shape, r0, c0)
        target_cells = {(r + dr, c + dc) for r, c in source_cells}
        if source_cells & target_cells:
            continue

        marker_positions = [
            (r, c)
            for r in range(h)
            for c in range(w)
            if 0 <= r + dr < h and 0 <= c + dc < w
            and (r, c) not in source_cells
            and (r, c) not in target_cells
            and (r + dr, c + dc) not in source_cells
            and (r + dr, c + dc) not in target_cells
        ]
        if not marker_positions:
            continue
        p1 = rng.choice(marker_positions)
        p2 = (p1[0] + dr, p1[1] + dc)

        grid = full_grid(h, w, 0)
        grid[p1[0]][p1[1]] = 1
        grid[p2[0]][p2[1]] = 2
        for r, c in source_cells:
            grid[r][c] = 3
        return grid

    raise ValueError("could not place vector translation instance")
