"""Generator for arc_puzzle_bank_21_set23_bundle:easy_p05.

Solid 2x2 squares bloom one same-color cell from each diagonal corner.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_squares,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_squares, single_cell, on_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75837d4fa905"
VERSION = "1.1.0"
TASK_ID = "75837d4fa905"
SUMMARY = "Solid 2x2 squares bloom one same-color cell from each diagonal corner."

INVARIANTS = [
    "background is 0",
    "each object is an isolated solid monochrome 2x2 block",
    "each block has empty diagonal corner cells available for blooming",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_squares", "single_cell", "on_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_squares":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "isolated_2x2_squares",
                       "valid": "isolated_2x2_squares"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _footprint(r: int, c: int) -> set[tuple[int, int]]:
    return {(rr, cc) for rr in range(r - 1, r + 3) for cc in range(c - 1, c + 3)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        square_count = ctx.draw_int("square_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        square_count = ctx.draw_int("square_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        square_count = ctx.draw_int("square_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    anchors = [(r, c) for r in range(1, h - 2) for c in range(1, w - 2)]
    rng.shuffle(anchors)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(square_count, 9))
    occupied: set[tuple[int, int]] = set()

    placed = 0
    for r, c in anchors:
        footprint = _footprint(r, c)
        if footprint & occupied:
            continue
        color = colors[placed % len(colors)]
        for rr in (r, r + 1):
            for cc in (c, c + 1):
                grid[rr][cc] = color
        occupied |= footprint
        placed += 1
        if placed >= square_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_squares":
        # blank → no 2x2 squares to bloom from
        return g
    if name == "single_cell":
        # singleton cells → not 2x2 squares
        g[3][3] = 4; g[5][6] = 6
        return g
    if name == "on_edge":
        # 2x2 at corner → diagonal blooms go out of bounds
        for r in range(2):
            for c in range(2):
                g[r][c] = 4
        return g
    return g
