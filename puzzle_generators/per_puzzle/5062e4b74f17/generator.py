"""Generator for f9d67f8b - radius-4 texture inpainting trigger.

Combinatorial axes (8): grid_size, palette_kind, patch_variant, bg_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_damage, no_texture, full_damage.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "5062e4b74f17"
VERSION = "1.1.0"
TASK_ID = "5062e4b74f17"
SUMMARY = "A 9x9 nonzero texture window contains maroon damage at the center."

INVARIANTS = [
    "no black cells are used",
    "color 9 marks the damaged center region",
    "the active 9x9 context is fully in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_damage", "no_texture", "full_damage")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "patch_variant":  {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "bg_color":       {"type": "int", "default": "rng 1..8", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 5..7", "valid": "5..9"},
    "position_bias":  {"type": "str", "default": "patch_in_textured_field",
                       "valid": "patch_in_textured_field"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..7", "valid": "5..9"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATCHES = [
    [
        [1, 1, 8, 6, 4, 6, 8, 2, 8],
        [4, 6, 7, 4, 3, 3, 8, 8, 2],
        [6, 4, 4, 6, 3, 3, 8, 8, 8],
        [2, 3, 4, 6, 1, 1, 2, 2, 1],
        [3, 2, 6, 4, 9, 9, 9, 9, 9],
        [8, 7, 4, 6, 9, 9, 9, 9, 9],
        [7, 8, 6, 6, 9, 9, 9, 9, 9],
        [7, 4, 5, 5, 1, 1, 4, 6, 1],
        [4, 7, 5, 5, 1, 1, 6, 4, 1],
    ],
    [
        [1, 2, 3, 4, 7, 7, 4, 9, 9],
        [9, 9, 9, 9, 9, 7, 8, 9, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9],
        [8, 6, 9, 9, 9, 9, 9, 9, 9],
        [8, 6, 9, 9, 9, 9, 9, 9, 9],
        [1, 5, 9, 9, 9, 9, 9, 9, 6],
        [1, 5, 9, 9, 9, 9, 9, 9, 4],
        [7, 1, 1, 6, 4, 1, 1, 8, 6],
        [1, 1, 1, 4, 6, 1, 1, 6, 8],
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
    g = full_grid(size, size, rng.choice([1, 3, 4, 6, 8]))
    patch = [row[:] for row in rng.choice(_PATCHES)]
    side = len(patch)
    paste(g, patch, rng.randint(1, size - side - 1), rng.randint(1, size - side - 1))
    return g


def _draw_from_degenerate(name, rng):
    size = 12
    g = full_grid(size, size, 4)
    if name == "no_damage":
        # textured patch but no color-9 damage region → nothing to inpaint
        clean_patch = [[1, 2, 3, 4, 7, 7, 4, 1, 1],
                       [3, 5, 8, 6, 4, 6, 8, 2, 8],
                       [4, 6, 7, 4, 3, 3, 8, 8, 2],
                       [6, 4, 4, 6, 3, 3, 8, 8, 8],
                       [2, 3, 4, 6, 1, 1, 2, 2, 1],
                       [3, 2, 6, 4, 5, 6, 7, 8, 4],
                       [8, 7, 4, 6, 7, 8, 6, 4, 6],
                       [7, 4, 5, 5, 1, 1, 4, 6, 1],
                       [4, 7, 5, 5, 1, 1, 6, 4, 1]]
        paste(g, clean_patch, 1, 1)
        return g
    if name == "no_texture":
        # damage region (color 9) without surrounding texture → can't infer fill
        for r in range(4, 7):
            for c in range(4, 7):
                g[r][c] = 9
        return g
    if name == "full_damage":
        # entire patch is color 9 → no surrounding texture to inpaint from
        for r in range(1, 10):
            for c in range(1, 10):
                g[r][c] = 9
        return g
    return g
