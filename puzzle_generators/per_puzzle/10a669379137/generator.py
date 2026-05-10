"""Generator for 3ad05f52 — maze with marker, ray-fill + wide-zone bridge.

Rule (per the canonical Racket): the input has cyan(8) walls forming a maze
structure plus a single marker color (a 3x3 block) inside one of the rooms.
The output fills:
  * cells reachable from the marker by cardinal "rays" that terminate at walls
    (or grid edges if the corresponding row/col contains walls)
  * cells in "wide" cols/rows (cols/rows with no walls) between the min and
    max painted rows/cols — the "min fill in the SUPER WIDE gap"

Per-puzzle variation: random grid size, random maze patch placement,
random marker color and position.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste, set_cell

GENERATOR_ID = "10a669379137"
VERSION = "2.0.0"
TASK_ID = "10a669379137"
SUMMARY = (
    "Cyan(8) maze walls + single 3x3 marker block. Output fills via cardinal "
    "ray-expansion bounded by walls, plus wide-axis bridge fill between "
    "min/max painted positions in wall-less cols/rows."
)

INVARIANTS = [
    "background is 0",
    "exactly one wall color (most-frequent non-bg) and exactly one marker color",
    "the maze structure forms at least one bounded room containing the marker",
    "marker is a 3x3 solid block inside a wall-bounded room",
]

AXES = {
    "grid_size":   {"type": "int", "default": "rng 18..26", "valid": "14..30"},
    "marker_color": {"type": "int", "default": "rng 1..9", "valid": "1..9 except 8"},
}

# 11x11 maze patch with a 2x3 grid of 3x3 rooms separated by walls.
# Internal corridors (gaps in walls) follow the canonical structure.
_MAZE_PATCH = [
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 0, 0, 0, 8, 0, 0, 0, 8, 0, 8],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [8, 0, 0, 0, 8, 0, 0, 0, 8, 0, 8],
    [8, 8, 0, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 0, 0, 0, 8, 0, 0, 0, 8, 0, 8],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
    [8, 0, 0, 0, 8, 0, 0, 0, 8, 0, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
]

# Candidate room top-left corners (3x3 rooms inside the patch).
_ROOM_POSITIONS = [
    (1, 1), (1, 5), (5, 1), (5, 5),
]


def _stamp_marker(g, anchor_r, anchor_c, color):
    for dr in range(3):
        for dc in range(3):
            set_cell(g, anchor_r + dr, anchor_c + dc, color)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")

    H = ctx.draw_int("grid_size", 18, 26)
    W = H + rng.randint(-2, 2)
    H = max(14, min(30, H))
    W = max(14, min(30, W))

    patch_h = len(_MAZE_PATCH)
    patch_w = len(_MAZE_PATCH[0])
    patch_r = rng.randint(1, H - patch_h - 1)
    patch_c = rng.randint(1, W - patch_w - 1)

    g = full_grid(H, W, 0)
    paste(g, _MAZE_PATCH, patch_r, patch_c)

    marker_color = ctx.draw_int("marker_color", 1, 9)
    if marker_color == 8:
        marker_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])

    room_local = rng.choice(_ROOM_POSITIONS)
    marker_r = patch_r + room_local[0]
    marker_c = patch_c + room_local[1]
    _stamp_marker(g, marker_r, marker_c, marker_color)

    return g
