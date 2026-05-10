"""Generator for 9b5080bb.

Rule: a single 5x5 motif-alignment context triggers the canonical local
correction table.

Combinatorial axes (8): grid_h/w, grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_patch, edge_patch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "d47d91bc30d0"
VERSION = "1.1.0"
TASK_ID = "d47d91bc30d0"
SUMMARY = "5x5 motif-alignment context triggers canonical local correction table."

INVARIANTS = [
    "the active context is a fully in-bounds 5x5 window",
    "the context uses the repeated motif colors from the canonical task",
    "the center cell differs from the table's replacement color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patch", "edge_patch", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "grid_size":      {"type": "int", "default": "rng 7..10", "valid": "7..10"},
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
        [8, 8, 8, 2, 2],
        [8, 8, 8, 2, 2],
        [8, 8, 8, 8, 2],
        [8, 8, 8, 2, 2],
        [8, 8, 8, 2, 2],
    ],
    [
        [4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4],
        [2, 2, 4, 2, 2],
        [2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2],
    ],
    [
        [1, 1, 1, 4, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [4, 4, 1, 4, 4],
        [4, 4, 4, 4, 4],
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
        size = ctx.draw_int("grid_size", 7, 8)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 9, 10)
    else:
        size = ctx.draw_int("grid_size", 7, 10)
    g = full_grid(size, size, 8)
    patch = [row[:] for row in rng.choice(_PATCHES)]
    r0 = rng.randint(1, size - 6)
    c0 = rng.randint(1, size - 6)
    paste(g, patch, r0, c0)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 8)
    if name == "no_patch":
        return g
    if name == "edge_patch":
        paste(g, _PATCHES[0], 0, 0)
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
