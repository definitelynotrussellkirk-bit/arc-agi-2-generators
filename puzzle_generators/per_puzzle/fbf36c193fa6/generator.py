"""Generator for 212895b5 - radius-3 cyan/gray diagonal fill trigger.

Combinatorial axes (8): grid_h, grid_w, palette_kind, patch_index,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_patch, multiple_patches, patch_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "fbf36c193fa6"
VERSION = "1.1.0"
TASK_ID = "fbf36c193fa6"
SUMMARY = "A 7x7 gray/cyan context triggers one magenta local fill."

INVARIANTS = [
    "background is 0",
    "the active 7x7 context is fully in bounds",
    "gray or cyan cells form the local ray/fill cue",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_patch", "multiple_patches", "patch_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

_PATCHES = [
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 8, 8, 8, 0, 0],
        [0, 0, 8, 8, 8, 0, 0],
    ],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "patch_index":    {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior_pasted",
                       "valid": "interior_pasted"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        # empty grid → no trigger context, rule has no anchor
        return g
    if name == "multiple_patches":
        # two patches → invariant says exactly one, rule output ambiguous
        paste(g, _PATCHES[0], 0, 0)
        paste(g, _PATCHES[1], 4, 4)
        return g
    if name == "patch_at_edge":
        # patch flush against bottom-right edge → trigger has no room to fill outward
        paste(g, _PATCHES[0], size - 7, size - 7)
        return g
    return g
