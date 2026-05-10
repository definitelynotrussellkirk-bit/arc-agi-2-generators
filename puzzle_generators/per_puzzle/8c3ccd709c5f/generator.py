"""Generator for arc_puzzle_bank_21_set16_s:S16_H6.

Rule: two color-1 markers and two color-2 markers define a rectangular
span. The rule crops the unique non-marker object fully contained in
that span.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_color_1, no_color_2, no_target_in_span.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8c3ccd709c5f"
VERSION = "1.1.0"
TASK_ID = "8c3ccd709c5f"
SUMMARY = "Parallel marker pairs bound the band containing the target object."

INVARIANTS = [
    "color 1 and color 2 each appear exactly twice",
    "the color-1 pair defines the span orientation",
    "exactly one non-marker object lies completely within the marker span",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_color_1", "no_color_2", "no_target_in_span")
HELPFUL_TEXTURES = PALETTE_KINDS

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_marker_corners",
                       "valid": "fixed_marker_corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape_idx = ctx.draw_int("shape", 0, 0)
    elif difficulty == "hard":
        shape_idx = ctx.draw_int("shape", 1, 2)
    else:
        shape_idx = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
    g = full_grid(13, 15, 0)
    r0, r1 = 2, 9
    c0, c1 = 2, 11
    g[r0][c0] = 1
    g[r0][c1] = 1
    g[r1][c0] = 2
    g[r1][c1] = 2
    cells = _SHAPES[shape_idx]
    color = rng.choice([3, 4, 5, 6, 7, 8, 9])
    for r, c in cells:
        g[4 + r][5 + c] = color
    g[11][1] = 9
    g[11][2] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 15, 0)
    if name == "no_color_1":
        # only color-2 pair → span orientation undefined
        g[9][2] = 2; g[9][11] = 2
        for r, c in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[4 + r][5 + c] = 4
        return g
    if name == "no_color_2":
        # only color-1 pair → span has no closing edge
        g[2][2] = 1; g[2][11] = 1
        for r, c in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[4 + r][5 + c] = 4
        return g
    if name == "no_target_in_span":
        # markers present but no non-marker object inside the band → rule has no crop target
        g[2][2] = 1; g[2][11] = 1
        g[9][2] = 2; g[9][11] = 2
        g[11][1] = 9; g[11][2] = 9
        return g
    return g
