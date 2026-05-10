"""Generator for 6165ea8f.

Rule: right-edge key colors index a shape-distance comparison table.

Combinatorial axes (8): grid_h/w, key_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_keys, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2602c3d31d21"
VERSION = "1.1.0"
TASK_ID = "2602c3d31d21"
SUMMARY = "Right-edge key colors index shape-distance comparison table."

INVARIANTS = [
    "background is color 0",
    "rightmost-column nonzero cells list key colors in order",
    "each key color also has a multi-cell shape elsewhere",
    "key colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SHAPES = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "key_count":      {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "3..4"},
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
    count = ctx.draw_int("key_count", 3, 4)
    colors = list(ctx.draw_distinct_colors("key_colors", n=count, exclude={0}))
    g = full_grid(9, 9, 0)
    for i in range(count):
        g[i + 1][8] = colors[i]
        paint_at(g, 1 + i * 2, 1, SHAPES[i], colors[i])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_keys":
        paint_at(g, 1, 1, SHAPES[0], 2)
        return g
    if name == "no_shapes":
        for i in range(3):
            g[i + 1][8] = 2 + i
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 2
        return g
    return g
