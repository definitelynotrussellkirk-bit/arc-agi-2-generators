"""Generator for arc_puzzle_bank_sixth_21_bundle:hard_38_shifted_overlay_count_map.

A multi-cell template contains a 9 anchor.  Other singleton 9 markers receive
shifted copies of that template under the canonical count-map rule.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "03000b260ae0"
VERSION = "1.1.0"
TASK_ID = "03000b260ae0"

SUMMARY = "Template component with an anchor 9, plus singleton 9 copy markers."

INVARIANTS = [
    "background is 0",
    "one connected nonzero template component contains exactly one 9 anchor",
    "all other 9 cells are isolated singleton markers",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "grid_w": {"type": "int", "default": "rng 12..15", "valid": "10..17"},
    "n_markers": {"type": "int", "default": "rng 2..4", "valid": "1..5"},
}

TEMPLATES = [
    (((0, 0), (0, 1), (1, 1), (2, 1)), (0, 1)),
    (((0, 0), (1, 0), (1, 1), (1, 2)), (1, 0)),
    (((0, 1), (1, 0), (1, 1), (2, 1)), (1, 1)),
    (((0, 0), (0, 1), (1, 0), (2, 0)), (0, 0)),
]


def _too_close(pos, taken):
    r, c = pos
    return any(abs(r - tr) <= 1 and abs(c - tc) <= 1 for tr, tc in taken)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 10, 12)
    w = ctx.draw_int("grid_w", 12, 15)
    n_markers = ctx.draw_int("n_markers", 2, 4)
    rng = ctx.draw_rng("layout")

    grid = full_grid(h, w, 0)
    cells, anchor = rng.choice(TEMPLATES)
    top = rng.randint(0, 1)
    left = rng.randint(1, 4)
    taken = set()
    for dr, dc in cells:
        r = top + dr
        c = left + dc
        grid[r][c] = 9 if (dr, dc) == anchor else 7
        taken.add((r, c))

    candidates = [
        (r, c)
        for r in range(h)
        for c in range(w)
        if grid[r][c] == 0 and not _too_close((r, c), taken)
    ]
    rng.shuffle(candidates)
    markers = []
    for pos in candidates:
        if _too_close(pos, markers):
            continue
        markers.append(pos)
        if len(markers) == n_markers:
            break
    if len(markers) < n_markers:
        raise ValueError("could not place singleton 9 markers")

    for r, c in markers:
        grid[r][c] = 9

    return grid
