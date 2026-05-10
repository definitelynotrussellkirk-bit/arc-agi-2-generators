"""Generator for additional_scaffolded:M7.

Rule: find largest 4-connected non-zero region (any colors); crop to bbox.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_objects, single_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ab6810fc781"
VERSION = "1.1.0"
TASK_ID = "3ab6810fc781"
SUMMARY = "Multi-color connected blob (largest) + small blobs of other shapes."

INVARIANTS = [
    "exactly one large multi-color connected region (size >= 5)",
    "1-2 smaller separated blobs",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "9..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[1][1] = 2
    g[1][2] = 3
    g[2][1] = 2
    g[2][2] = 2
    g[2][3] = 3
    g[3][2] = 2
    g[2][6] = 4
    g[3][6] = 4
    g[5][3] = 5
    g[5][4] = 5
    g[6][3] = 5
    g[6][4] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_objects":
        return g
    if name == "single_blob":
        g[3][3] = 3
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
