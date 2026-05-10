"""Generator for arc_puzzle_bank_fourteenth_21_bundle:easy_95_draw_rectangle_borders_from_diagonal_corners.

Rule: each unique-color opposite-corner pair has its rectangle outline
drawn in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corners, single_corner, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8d2cfdfec79c"
VERSION = "1.1.0"
TASK_ID = "8d2cfdfec79c"

SUMMARY = "Place disjoint same-color opposite-corner pairs for rectangle-border drawing."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "same-color cells are opposite corners of an axis-aligned rectangle",
    "rectangle footprints are disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "single_corner", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= rectangles", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "disjoint_corner_pairs",
                       "valid": "disjoint_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= rectangles", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("rectangles", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        target = ctx.draw_int("rectangles", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        target = min(ctx.draw_int("rectangles", 2, 3), 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        rh = rng.randint(3, min(5, h))
        rw = rng.randint(3, min(6, w))
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        r1 = r0 + rh - 1
        c1 = c0 + rw - 1
        footprint = {(r, c) for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)}
        if footprint & reserved:
            continue
        color = colors[placed]
        if rng.randrange(2):
            g[r0][c0] = color
            g[r1][c1] = color
        else:
            g[r0][c1] = color
            g[r1][c0] = color
        reserved.update(footprint)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # Empty grid — no opposite-corner pair to outline.
        return g
    if name == "single_corner":
        # Each color appears once — no pair, no rectangle defined.
        g[2][2] = 4
        g[6][7] = 6
        return g
    if name == "collinear_pair":
        # Same-color cells on the same row/column — degenerate to a
        # line, no 2D outline can be drawn.
        g[2][1] = 4; g[2][7] = 4
        g[1][3] = 6; g[6][3] = 6
        return g
    return g
