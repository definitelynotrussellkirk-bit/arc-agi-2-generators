"""Generator for arc_puzzle_bank_21_set13_s:S13_M3 — header count picks symmetry class.

Rule: a blue-count header chooses a symmetry class whose first body
object is cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, symmetry_code,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_header, no_matching_class, missing_class.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "0a2588a98f5b"
VERSION = "1.1.0"
TASK_ID = "0a2588a98f5b"

SUMMARY = "A blue-count header chooses a symmetry class whose first body object is cropped."

INVARIANTS = [
    "background is 0",
    "the top row encodes one of four symmetry classes",
    "the body contains one object from each encoded symmetry class",
    "objects are separated so their intrinsic symmetry classes are unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "no_matching_class", "missing_class")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "symmetry_code":  {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "header_with_classes",
                       "valid": "header_with_classes"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

VERT_ONLY = [(0, 0), (0, 1), (0, 2), (1, 1)]
HORIZ_ONLY = [(0, 0), (1, 0), (2, 0), (1, 1)]
BOTH = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
ASYM = [(0, 0), (1, 0), (1, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    code = ctx.draw_int("symmetry_code", 1, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    for c in range(code):
        g[0][c] = 1

    r0 = rng.randint(2, 3)
    paint_at(g, r0, 1, VERT_ONLY, 2)
    paint_at(g, r0, 6, HORIZ_ONLY, 3)
    paint_at(g, h - 4, 1, BOTH, 4)
    paint_at(g, h - 3, w - 4, ASYM, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_header":
        # body objects but no header → no symmetry class encoded
        paint_at(g, 2, 1, VERT_ONLY, 2)
        paint_at(g, 2, 6, HORIZ_ONLY, 3)
        paint_at(g, h - 4, 1, BOTH, 4)
        paint_at(g, h - 3, w - 4, ASYM, 6)
        return g
    if name == "no_matching_class":
        # header encodes class 1 but body has no object of that class
        g[0][0] = 1
        paint_at(g, 2, 1, BOTH, 4)
        paint_at(g, h - 3, w - 4, ASYM, 6)
        return g
    if name == "missing_class":
        # header encodes class 3 but body skips that class
        g[0][0] = 1; g[0][1] = 1; g[0][2] = 1
        paint_at(g, 2, 1, VERT_ONLY, 2)
        paint_at(g, 2, 6, HORIZ_ONLY, 3)
        paint_at(g, h - 3, w - 4, ASYM, 6)
        return g
    return g
