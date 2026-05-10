"""Generator for 96a8c0cd - radius-6 contour drawing trigger.

Rule: a 13x13 blue/green contour context triggers one red contour pixel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, grid_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_patch, patch_at_corner, blank_patch.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "defba1ab4f90"
VERSION = "1.1.0"
TASK_ID = "defba1ab4f90"
SUMMARY = "A 13x13 blue/green contour context triggers one red contour pixel."

INVARIANTS = [
    "background is 0",
    "colors 1 and 3 form the local contour source",
    "the active 13x13 context is fully in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_patch", "patch_at_corner", "blank_patch")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 15..18", "valid": "13..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "interior_13x13_patch",
                       "valid": "interior_13x13_patch"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATCH = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        size = ctx.draw_int("grid_size", 15, 15)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 17, 18)
    else:
        size = ctx.draw_int("grid_size", 15, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(size, size, 0)
    side = len(_PATCH)
    paste(g, _PATCH, rng.randint(1, size - side - 1), rng.randint(1, size - side - 1))
    return g


def _draw_from_degenerate(name, rng):
    size = 16
    side = len(_PATCH)
    if name == "no_patch":
        # blank → no contour context, no red pixel to paint
        return full_grid(size, size, 0)
    if name == "patch_at_corner":
        # patch at (0,0) instead of interior → invariant says "fully in bounds with margin"
        g = full_grid(size, size, 0)
        paste(g, _PATCH, 0, 0)   # touches edge
        return g
    if name == "blank_patch":
        # patch position with all-0 patch → no contour to detect
        return full_grid(size, size, 0)
    return full_grid(size, size, 0)
