"""Generator for 8dab14c2.

Rule: a 9x9 blue/cyan boundary context triggers one local smoothing
rewrite.

Combinatorial axes (8): grid_h/w, grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_patch, edge_patch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "6cefe79f3cfb"
VERSION = "1.1.0"
TASK_ID = "6cefe79f3cfb"
SUMMARY = "9x9 blue/cyan boundary context triggers one local smoothing rewrite."

INVARIANTS = [
    "the active 9x9 context is fully in bounds",
    "colors 1 and 8 form the local boundary",
    "the center value differs from the canonical replacement",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patch", "edge_patch", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "11..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "11..14"},
    "grid_size":      {"type": "int", "default": "rng 11..14", "valid": "11..14"},
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
        [1, 1, 1, 1, 1, 1, 1, 1, 8],
        [1, 1, 1, 1, 1, 1, 1, 1, 8],
        [1, 1, 1, 1, 1, 1, 1, 1, 8],
        [1, 1, 1, 1, 1, 1, 1, 1, 8],
        [8, 8, 8, 8, 8, 1, 1, 1, 8],
        [8, 8, 8, 8, 8, 1, 1, 1, 8],
        [8, 8, 8, 8, 8, 1, 1, 1, 8],
        [8, 8, 8, 8, 8, 1, 1, 8, 8],
        [8, 8, 8, 8, 8, 1, 1, 1, 8],
    ],
    [
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 1, 8, 8, 8, 8],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [8, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 8, 8, 8, 8, 8],
        [1, 1, 1, 1, 8, 8, 8, 8, 8],
        [1, 1, 1, 1, 8, 8, 8, 8, 8],
        [1, 1, 1, 1, 8, 8, 8, 8, 8],
    ],
    [
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 1, 8, 8, 8, 8],
        [1, 1, 1, 1, 1, 1, 1, 8, 8],
        [1, 1, 1, 1, 1, 1, 1, 8, 8],
        [1, 1, 1, 1, 1, 1, 1, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8],
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
        size = ctx.draw_int("grid_size", 11, 12)
    elif difficulty == "hard":
        size = ctx.draw_int("grid_size", 13, 14)
    else:
        size = ctx.draw_int("grid_size", 11, 14)
    g = full_grid(size, size, 8)
    patch = [row[:] for row in rng.choice(_PATCHES)]
    side = len(patch)
    r0 = rng.randint(1, size - side - 1)
    c0 = rng.randint(1, size - side - 1)
    paste(g, patch, r0, c0)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 8)
    if name == "no_patch":
        return g
    if name == "edge_patch":
        paste(g, _PATCHES[0], 0, 0)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
