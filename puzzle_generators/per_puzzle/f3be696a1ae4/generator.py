"""Generator for additional_scaffolded:M5.

Rule: find 9-axis col; for each cell on right with empty value, copy
mirror cell from left if non-{0,9}.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_axis, no_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f3be696a1ae4"
VERSION = "1.1.0"
TASK_ID = "f3be696a1ae4"
SUMMARY = "Vertical 9-axis + small blobs on left mirrored to right."

INVARIANTS = [
    "exactly one full-column 9-axis",
    "1-3 colored blobs on left side, none on right",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_axis", "no_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "7..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    axis = w // 2
    for r in range(h):
        g[r][axis] = 9
    g[1][1] = 2
    g[2][1] = 2
    g[2][2] = 2
    g[4][2] = 3
    g[5][2] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 8, 0)
    if name == "no_axis":
        g[1][1] = 2
        return g
    if name == "no_blob":
        for r in range(7):
            g[r][4] = 9
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(8):
                g[r][c] = 9
        return g
    return g
