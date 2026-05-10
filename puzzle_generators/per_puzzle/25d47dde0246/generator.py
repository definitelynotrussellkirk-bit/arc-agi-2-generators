"""Generator for arc_additional_puzzle_bank_volume15:E104.

Rule: subgrid bounded by min/max row/col of all non-bg cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_object, touches_border, two_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "25d47dde0246"
VERSION = "1.1.0"
TASK_ID = "25d47dde0246"
SUMMARY = "Single small shape near grid center, padding around it."

INVARIANTS = [
    "exactly 1 small connected shape",
    "≥1 padding row/col on every side",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_object", "touches_border", "two_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "str", "default": "rng_4_options",
                       "valid": "rng_4_options"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "centered_with_padding",
                       "valid": "centered_with_padding"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "small_blob", "valid": "small_blob"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shapes = [
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 0)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1)],
    ]
    s = rng.choice(shapes)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    top = rng.randint(1, h - 4)
    left = rng.randint(1, w - 4)
    paint_at(g, top, left, s, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_object":
        # empty grid — bbox undefined
        return g
    if name == "touches_border":
        # shape touches the grid edge → padding invariant fails
        for r, c in [(0, 0), (0, 1), (1, 0)]:
            g[r][c] = 4
        return g
    if name == "two_objects":
        # two separate blobs → bbox spans both, includes empty cells inside
        for r, c in [(2, 2), (2, 3), (3, 2)]:
            g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 7)]:
            g[r][c] = 4
        return g
    return g
