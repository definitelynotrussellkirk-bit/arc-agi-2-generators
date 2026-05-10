"""Generator for 825aa9e9.

Rule: a 7x7 floor/support context triggers one local recentering rewrite.

Combinatorial axes (8): grid_h/w, grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_patch, edge_patch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "3d9d2f9baa4e"
VERSION = "1.1.0"
TASK_ID = "3d9d2f9baa4e"
SUMMARY = "7x7 floor/support context triggers one local recentering rewrite."

INVARIANTS = [
    "color 7 is the field/floor color",
    "colors 4 and 1 form the object/support signature",
    "the active context is fully in bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patch", "edge_patch", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "9..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "9..12"},
    "grid_size":      {"type": "int", "default": "rng 9..12", "valid": "9..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATCHES = [
    [
        [4, 4, 7, 7, 7, 7, 7],
        [7, 4, 7, 4, 4, 4, 7],
        [4, 4, 7, 4, 4, 4, 7],
        [7, 7, 7, 7, 4, 7, 7],
        [7, 7, 7, 7, 4, 7, 7],
        [7, 7, 7, 7, 7, 7, 1],
        [7, 7, 7, 7, 7, 7, 1],
    ],
    [
        [7, 4, 7, 4, 7, 4, 4],
        [7, 4, 4, 4, 7, 4, 4],
        [7, 7, 7, 7, 7, 7, 4],
        [7, 7, 7, 7, 7, 7, 4],
        [7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 1, 1],
    ],
    [
        [7, 4, 4, 4, 7, 4, 4],
        [7, 7, 7, 7, 7, 7, 4],
        [7, 7, 7, 7, 7, 7, 4],
        [7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        size = ctx.draw_int("grid_size", 9, 10)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 11, 12)
    else:
        size = ctx.draw_int("grid_size", 9, 12)
    g = full_grid(size, size, 7)
    patch = [row[:] for row in rng.choice(_PATCHES)]
    side = len(patch)
    r0 = rng.randint(1, size - side - 1)
    c0 = rng.randint(1, size - side - 1)
    paste(g, patch, r0, c0)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 7)
    if name == "no_patch":
        return g
    if name == "edge_patch":
        paste(g, _PATCHES[0], 0, 0)
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 4
        return g
    return g
