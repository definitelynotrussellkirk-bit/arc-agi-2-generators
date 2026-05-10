"""Generator for arc_puzzle_bank_21_set18_bundle:easy_p04.

Rule: each connected object is erased except for the four corners of
its bounding box.

Combinatorial axes (8): grid_h, grid_w, palette_kind, object_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: line_objects, single_cell_objects, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "58cc346198c0"
VERSION = "1.1.0"
TASK_ID = "58cc346198c0"
SUMMARY = "Separated connected L-shapes whose bbox corners are retained."

INVARIANTS = [
    "background is 0",
    "each object is one connected same-color component",
    "each object has bbox height and width at least two",
    "objects are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("line_objects", "single_cell_objects", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_count":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread_L_shapes",
                       "valid": "spread_L_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _zone(r, c, rh, rw):
    return {(rr, cc) for rr in range(r - 1, r + rh + 1) for cc in range(c - 1, c + rw + 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        object_count = ctx.draw_int("object_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        object_count = ctx.draw_int("object_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        object_count = ctx.draw_int("object_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=object_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            rh = rng.randint(2, 4)
            rw = rng.randint(2, 4)
            r = rng.randint(0, h - rh)
            c = rng.randint(0, w - rw)
            zone = _zone(r, c, rh, rw)
            if zone & occupied:
                continue
            for rr in range(r, r + rh):
                g[rr][c] = color
            for cc in range(c, c + rw):
                g[r + rh - 1][cc] = color
            occupied |= zone
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "line_objects":
        # 1×N or N×1 lines → bbox has only 2 distinct corners
        for c in range(1, 6): g[2][c] = 4
        for r in range(4, 8): g[r][8] = 6
        return g
    if name == "single_cell_objects":
        # 1x1 objects → bbox has 1 distinct corner; rule keeps the cell, identity
        g[2][3] = 4; g[5][7] = 6; g[6][1] = 3
        return g
    if name == "no_objects":
        # blank grid → rule has nothing to extract
        return g
    return g
