"""Generator for 93c31fbe - radius-3 sparse motif repair trigger.

Combinatorial axes (8): grid_h, grid_w, palette_kind, patch_index,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_patch, multiple_patches, all_zero_patch.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "d5a059b0f3a6"
VERSION = "1.1.0"
TASK_ID = "d5a059b0f3a6"
SUMMARY = "A 7x7 sparse anchor/motif context triggers one color-1 local repair."

INVARIANTS = [
    "background is 0",
    "colors 1 and 8 form repeated sparse anchors",
    "the active 7x7 context is fully in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_patch", "multiple_patches", "all_zero_patch")
HELPFUL_TEXTURES = PALETTE_KINDS

_PATCHES = [
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 8, 8, 0],
        [0, 1, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 8, 0],
        [8, 0, 0, 0, 8, 8, 0],
    ],
    [
        [8, 0, 0, 0, 8, 8, 0],
        [0, 1, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 8, 0],
        [8, 0, 0, 0, 8, 8, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "patch_index":    {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "interior_pasted",
                       "valid": "interior_pasted"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    if difficulty == "easy":
        size = ctx.draw_int("grid_size", 9, 9)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 11, 12)
    else:
        size = ctx.draw_int("grid_size", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(size, size, 0)
    patch = [row[:] for row in rng.choice(_PATCHES)]
    side = len(patch)
    paste(g, patch, rng.randint(1, size - side - 1), rng.randint(1, size - side - 1))
    return g


def _draw_from_degenerate(name, rng):
    size = 11
    g = full_grid(size, size, 0)
    if name == "no_patch":
        # empty grid → no anchor/motif context, rule has no trigger
        return g
    if name == "multiple_patches":
        # two overlapping patches → rule expects exactly one trigger context
        paste(g, _PATCHES[0], 0, 0)
        paste(g, _PATCHES[1], 4, 4)
        return g
    if name == "all_zero_patch":
        # patch region is all 0 → no 1/8 anchors to drive repair
        for r in range(2, 9):
            for c in range(2, 9):
                g[r][c] = 0
        return g
    return g
