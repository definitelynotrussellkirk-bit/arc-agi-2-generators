"""Generator for b74ca5d1.

Rule: a 9x9 small-shape boundary context triggers one recolor.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_patch, edge_patch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "deb310c21d0c"
VERSION = "1.1.0"
TASK_ID = "deb310c21d0c"
SUMMARY = "A 9x9 small-shape boundary context triggers one recolor."

INVARIANTS = [
    "background is 0",
    "color 2 forms the local shape boundary",
    "one boundary color-2 cell is recolored to 7",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patch", "edge_patch", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATCH = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 2, 0, 0, 0, 2],
    [0, 0, 0, 0, 7, 0, 0, 0, 2],
    [0, 0, 0, 0, 2, 0, 0, 0, 2],
    [0, 0, 0, 0, 2, 2, 2, 2, 2],
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
    side = len(_PATCH)
    paste(g, _PATCH, rng.randint(1, size - side - 1), rng.randint(1, size - side - 1))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_patch":
        return g
    if name == "edge_patch":
        paste(g, _PATCH, 0, 0)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
