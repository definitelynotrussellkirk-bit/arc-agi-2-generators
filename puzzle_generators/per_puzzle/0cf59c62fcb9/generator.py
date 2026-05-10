"""Generator for arc_puzzle_bank_twentieth_21_bundle:hard_136_fill_chambers_by_nearest_seed_with_tie_break.

Color 8 forms walls.  Within each chamber, colored seeds determine the
nearest-seed fill under the canonical shortest-path rule.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0cf59c62fcb9"
VERSION = "1.1.0"
TASK_ID = "0cf59c62fcb9"

SUMMARY = "Compact wall-bounded chambers with seed colors for nearest-fill."

INVARIANTS = [
    "walls are color 8",
    "open chamber cells are 0 or seed colors",
    "each chamber contains at least one colored seed",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 7..8", "valid": "6..10"},
    "grid_w": {"type": "int", "default": "rng 9..11", "valid": "7..13"},
    "layout": {"type": "choice", "default": "rng vertical|horizontal|cross"},
}


def _room_cells(r1, c1, r2, c2):
    return [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]


def _seed_room(grid, cells, rng, colors):
    if len(cells) < 2:
        return
    count = min(len(cells) - 1, rng.randint(2, 3))
    positions = rng.sample(cells, count)
    seed_colors = rng.sample(colors, count)
    for (r, c), color in zip(positions, seed_colors):
        grid[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 7, 8)
    w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout_rng")

    requested = overrides.get("layout")
    if requested is not None:
        if requested not in {"vertical", "horizontal", "cross"}:
            raise ValueError("layout override must be vertical, horizontal, or cross")
        layout = requested
    else:
        layout = rng.choice(["vertical", "horizontal", "cross"])

    grid = full_grid(h, w, 8)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            grid[r][c] = 0

    rooms = [(1, 1, h - 2, w - 2)]
    if layout == "vertical":
        wall_c = rng.randint(3, w - 4)
        for r in range(1, h - 1):
            grid[r][wall_c] = 8
        rooms = [(1, 1, h - 2, wall_c - 1), (1, wall_c + 1, h - 2, w - 2)]
    elif layout == "horizontal":
        wall_r = rng.randint(3, h - 4) if h >= 8 else 3
        for c in range(1, w - 1):
            grid[wall_r][c] = 8
        rooms = [(1, 1, wall_r - 1, w - 2), (wall_r + 1, 1, h - 2, w - 2)]
    else:
        wall_r = rng.randint(3, h - 4) if h >= 8 else 3
        wall_c = rng.randint(3, w - 4)
        for c in range(1, w - 1):
            grid[wall_r][c] = 8
        for r in range(1, h - 1):
            grid[r][wall_c] = 8
        rooms = [
            (1, 1, wall_r - 1, wall_c - 1),
            (1, wall_c + 1, wall_r - 1, w - 2),
            (wall_r + 1, 1, h - 2, wall_c - 1),
            (wall_r + 1, wall_c + 1, h - 2, w - 2),
        ]

    colors = [2, 3, 4, 5, 6, 7, 9]
    for box in rooms:
        cells = _room_cells(*box)
        _seed_room(grid, cells, rng, colors)

    return grid
