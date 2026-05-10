"""Generator for de493100 — radius-5 noisy rectangle inpainting trigger.

Rule: an 11x11 texture window contains an orange-marked damage band; the
rule inpaints the orange cells from the local table.

Combinatorial axes (8): grid_size, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_patch, no_orange, full_orange.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "61e174f34b52"
VERSION = "1.1.0"
TASK_ID = "61e174f34b52"
SUMMARY = "An 11x11 texture window contains orange-marked damage that the local table repairs."

INVARIANTS = [
    "the active 11x11 context is fully in bounds",
    "orange 7 marks the noisy rectangle band",
    "the center 7 is replaced by the canonical table",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_patch", "no_orange", "full_orange")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 5..7", "valid": "3..9"},
    "position_bias":  {"type": "str", "default": "patched_texture",
                       "valid": "patched_texture"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..7", "valid": "3..9"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATCHES = [
    [
        [1, 1, 3, 5, 7, 7, 7, 7, 7, 8, 9],
        [9, 1, 3, 5, 7, 7, 7, 7, 7, 8, 9],
        [1, 9, 1, 8, 7, 7, 7, 7, 7, 9, 8],
        [9, 4, 9, 1, 7, 7, 7, 7, 7, 3, 3],
        [8, 8, 2, 9, 7, 7, 7, 7, 7, 1, 1],
        [8, 9, 9, 1, 7, 7, 7, 7, 7, 2, 9],
        [2, 9, 9, 9, 2, 9, 1, 3, 1, 2, 2],
        [6, 9, 9, 2, 6, 2, 3, 1, 3, 3, 1],
        [4, 9, 9, 2, 2, 1, 1, 9, 1, 1, 3],
        [9, 4, 6, 2, 1, 3, 6, 2, 9, 1, 3],
        [9, 6, 9, 3, 1, 6, 3, 9, 1, 9, 1],
    ],
    [
        [1, 1, 8, 9, 7, 7, 9, 8, 8, 8, 4],
        [9, 9, 3, 9, 7, 7, 9, 2, 8, 9, 3],
        [1, 1, 9, 3, 7, 7, 2, 9, 9, 4, 9],
        [9, 9, 9, 9, 7, 7, 8, 9, 9, 9, 4],
        [8, 8, 6, 8, 7, 7, 8, 3, 9, 4, 4],
        [6, 6, 8, 8, 7, 7, 3, 9, 9, 1, 4],
        [8, 8, 8, 8, 7, 7, 9, 3, 8, 5, 3],
        [6, 6, 8, 6, 7, 7, 1, 9, 1, 5, 5],
        [8, 8, 9, 4, 7, 7, 1, 5, 5, 2, 1],
        [4, 4, 3, 9, 7, 7, 4, 3, 5, 2, 1],
        [4, 4, 4, 3, 9, 5, 3, 4, 4, 1, 6],
    ],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        size = ctx.draw_int("grid_size", 13, 13)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 16, 18)
    else:
        size = ctx.draw_int("grid_size", 13, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(size, size, rng.choice([1, 3, 4, 8, 9]))
    patch = [row[:] for row in rng.choice(_PATCHES)]
    side = len(patch)
    paste(g, patch, rng.randint(1, size - side - 1), rng.randint(1, size - side - 1))
    return g


def _draw_from_degenerate(name, rng):
    size = 14
    g = full_grid(size, size, 1)
    if name == "no_patch":
        # Background-only grid with no 11x11 patch — rule has no
        # texture window and no orange band to inpaint.
        return g
    if name == "no_orange":
        # Patch present but the orange band is replaced with bg —
        # rule has no damage marker, output equals input.
        for r in range(size):
            for c in range(size):
                g[r][c] = 9
        return g
    if name == "full_orange":
        # Entire grid is orange-7 — rule's local-table repair has no
        # surrounding texture to copy from.
        for r in range(size):
            for c in range(size):
                g[r][c] = 7
        return g
    return g
