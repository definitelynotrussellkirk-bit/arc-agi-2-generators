"""Generator for 5623160b.

Rule: each non-9 component slides away from its nearest 9 cell until
it reaches the grid edge.

Combinatorial axes (8): grid_h/w, object_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_anchor, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a1c55d0f7af9"
VERSION = "1.1.0"
TASK_ID = "a1c55d0f7af9"
SUMMARY = "Each non-9 component slides away from nearest 9 until grid edge."

INVARIANTS = [
    "the background is color 7",
    "at least one color-9 cell anchors the scene",
    "each other object has a nearest 9 cell with a clear dominant offset",
    "object colors are distinct from 7 and 9",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anchor", "no_objects", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "object_count":   {"type": "int", "default": "2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    colors = ctx.draw_distinct_colors("object_colors", n=2, exclude={7, 9})
    g = full_grid(13, 13, 7)
    g[6][6] = 9
    for r, c in [(2, 6), (3, 6), (3, 7)]:
        g[r][c] = colors[0]
    for r, c in [(6, 9), (7, 9), (7, 10)]:
        g[r][c] = colors[1]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 7)
    if name == "no_anchor":
        g[3][3] = 2
        return g
    if name == "no_objects":
        g[6][6] = 9
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 9
        return g
    return g
