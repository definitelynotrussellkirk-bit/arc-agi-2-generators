"""Generator for arc_puzzle_bank_fifteenth21:H103.

Rule: a 1/2/3/4 marker selects the sweep direction. A colored object is
translated in that direction until the next step would hit an 8 wall or the
grid boundary; the output is the union of all swept object positions plus the
walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f13a4603318b"
VERSION = "1.1.0"
TASK_ID = "f13a4603318b"

SUMMARY = "Sweep a whole object in the direction named by a 1/2/3/4 marker."

INVARIANTS = [
    "background is 0",
    "exactly one 1/2/3/4 direction marker appears",
    "8 cells are immovable walls",
    "one connected object uses a non-marker, non-wall color",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 7..9", "valid": "7..9"},
    "grid_w": {"type": "int", "default": "rng 7..9", "valid": "7..9"},
    "direction": {"type": "choice", "default": "rng 1/2/3/4", "valid": "1..4"},
    "object_color": {"type": "color", "default": "rng excluding 0..4,8", "valid": "5/6/7/9"},
    "shape": {"type": "choice", "default": "rng small connected motifs", "valid": "0..4"},
    "steps_before_block": {"type": "int", "default": "rng 2..available", "valid": "2..5"},
}

DIRECTIONS = {
    1: (-1, 0),
    2: (1, 0),
    3: (0, -1),
    4: (0, 1),
}

SHAPES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
]


def _shape_size(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def _start_for_direction(rng, code, cells, h, w):
    shape_h, shape_w = _shape_size(cells)
    if code == 4:
        return rng.randint(1, h - shape_h - 1), 1
    if code == 3:
        return rng.randint(1, h - shape_h - 1), w - shape_w - 1
    if code == 2:
        return 1, rng.randint(1, w - shape_w - 1)
    return h - shape_h - 1, rng.randint(1, w - shape_w - 1)


def _max_steps_before_wall(code, r0, c0, cells, h, w):
    max_r = max(r for r, _ in cells)
    max_c = max(c for _, c in cells)
    if code == 4:
        return w - (c0 + max_c) - 2
    if code == 3:
        return c0 - 1
    if code == 2:
        return h - (r0 + max_r) - 2
    return r0 - 1


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
    w = ctx.draw_int("grid_w", 7, 9)
    code = ctx.draw_choice("direction", [1, 2, 3, 4])
    color = ctx.draw_color("object_color", exclude={0, 1, 2, 3, 4, 8})
    shape_index = ctx.draw_int("shape", 0, len(SHAPES) - 1)
    cells = SHAPES[shape_index]
    rng = ctx.draw_rng("layout")

    r0, c0 = _start_for_direction(rng, code, cells, h, w)
    max_steps = _max_steps_before_wall(code, r0, c0, cells, h, w)
    steps = ctx.draw_int("steps_before_block", 2, max_steps)
    dr, dc = DIRECTIONS[code]

    g = full_grid(h, w, 0)
    for r, c in cells:
        g[r0 + r][c0 + c] = color

    wall_shift = steps + 1
    wall_r, wall_c = cells[0]
    g[r0 + wall_r + dr * wall_shift][c0 + wall_c + dc * wall_shift] = 8

    marker_positions = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    for mr, mc in marker_positions:
        if g[mr][mc] == 0:
            g[mr][mc] = code
            return g
    raise ValueError("no free corner for direction marker")
