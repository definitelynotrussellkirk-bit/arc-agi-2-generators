"""Generator for f9a67cb5 - radius-4 maze path local trigger.

Combinatorial axes (8): grid_h, grid_w, palette_kind, patch_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, single_wall_row, walls_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "46c02325ed3b"
VERSION = "1.1.0"
TASK_ID = "46c02325ed3b"
SUMMARY = "A 9x9 cyan-wall maze context triggers one red path fill."

INVARIANTS = [
    "background is 0",
    "cyan 8 cells form local wall rows",
    "the active 9x9 context is fully in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "single_wall_row", "walls_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "patch_variant":  {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "patch_in_bounds",
                       "valid": "patch_in_bounds"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATCHES = [
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 8, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 8, 0, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 8, 0, 8, 8, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        size = ctx.draw_int("grid_size", 11, 12)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 13, 14)
    else:
        size = ctx.draw_int("grid_size", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(size, size, 0)
    patch = [row[:] for row in rng.choice(_PATCHES)]
    side = len(patch)
    paste(g, patch, rng.randint(1, size - side - 1), rng.randint(1, size - side - 1))
    return g


def _draw_from_degenerate(name, rng):
    size = 12
    g = full_grid(size, size, 0)
    if name == "no_walls":
        # blank → no maze structure to trigger path fill
        return g
    if name == "single_wall_row":
        # only one wall row → ambiguous radius-4 maze context
        for c in range(2, 11):
            g[5][c] = 8
        return g
    if name == "walls_at_edge":
        # patch at grid border → maze radius-4 frame would be out of bounds
        patch = [row[:] for row in _PATCHES[0]]
        side = len(patch)
        paste(g, patch, 0, 0)
        return g
    return g
