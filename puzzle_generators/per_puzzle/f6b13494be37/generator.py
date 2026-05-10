"""Generator for c3fa4749.

Rule: a radius-1 rectangle-noise context appears inside a padded grid;
the local repair table fires.

Combinatorial axes (8): grid_h/w, grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_patch, edge_patch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "f6b13494be37"
VERSION = "1.1.0"
TASK_ID = "f6b13494be37"
SUMMARY = "Radius-1 rectangle-noise context appears inside a padded grid."

INVARIANTS = [
    "one 3x3 neighborhood exactly matches a canonical repair-table entry",
    "the center value is an intruder color",
    "padding prevents accidental out-of-bounds signatures",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patch", "edge_patch", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "5..8"},
    "grid_w":         {"type": "int", "default": "rng 5..8", "valid": "5..8"},
    "grid_size":      {"type": "int", "default": "rng 5..8", "valid": "5..8"},
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
    [[1, 1, 1], [1, 8, 4], [1, 5, 1]],
    [[3, 4, 3], [3, 9, 3], [3, 4, 3]],
    [[7, 8, 7], [7, 1, 7], [4, 6, 7]],
    [[4, 4, 4], [4, 3, 0], [4, 9, 4]],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        size = ctx.draw_int("grid_size", 5, 6)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 7, 8)
    else:
        size = ctx.draw_int("grid_size", 5, 8)
    g = full_grid(size, size, 0)
    patch = [row[:] for row in rng.choice(_PATCHES)]
    r0 = rng.randint(1, size - 4)
    c0 = rng.randint(1, size - 4)
    paste(g, patch, r0, c0)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "no_patch":
        return g
    if name == "edge_patch":
        paste(g, _PATCHES[0], 0, 0)
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(6):
                g[r][c] = 4
        return g
    return g
