"""Generator for arc_puzzle_bank_fifteenth_21_bundle:easy_102_stamp_x_shapes_at_markers.

Rule: each interior nonzero singleton stamps a radius-1 X (center + 4 diagonals).

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, markers_at_edge, overlapping_x_footprints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d21c703c24c"
VERSION = "1.1.0"
TASK_ID = "5d21c703c24c"
SUMMARY = "Place isolated interior markers that stamp radius-1 X shapes."

INVARIANTS = [
    "background is 0",
    "markers are nonzero singleton cells",
    "markers are at least one cell from the border",
    "X footprints are disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "markers_at_edge", "overlapping_x_footprints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior_only",
                       "valid": "interior_only"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_X = [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("markers", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        target = ctx.draw_int("markers", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        footprint = {(r + dr, c + dc) for dr, dc in _X}
        if footprint & reserved:
            continue
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        reserved.update(footprint)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank grid → no X stamps emitted, output identical to input
        return g
    if name == "markers_at_edge":
        # markers on border row/col → X arms fall outside grid; rule undefined or clipped
        g[0][3] = 4
        g[5][0] = 6
        g[h - 1][7] = 3
        return g
    if name == "overlapping_x_footprints":
        # adjacent markers → X arms collide; ambiguous which color wins
        g[2][3] = 4
        g[3][4] = 6
        g[5][6] = 3
        g[6][7] = 8
        return g
    return g
