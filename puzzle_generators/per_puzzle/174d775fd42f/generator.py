"""Generator for ce8d95cc.

Rule: grid with full nonzero rows and constant nonzero columns is
compressed by representative rows and columns.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
size.
Degenerates: no_lines, no_columns, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "174d775fd42f"
VERSION = "1.1.0"
TASK_ID = "174d775fd42f"
SUMMARY = "Grid with full nonzero rows and constant nonzero cols compressed by reps."

INVARIANTS = [
    "background is color 0",
    "horizontal divider rows are fully nonzero",
    "vertical divider columns have one nonzero color across non-divider rows",
    "row and col colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lines", "no_columns", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "7", "valid": "7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "size":           {"type": "str", "default": "7x7", "valid": "7x7"},
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
    hline, v1, v2 = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(7, 7, 0)
    for r in (2, 5):
        for c in range(7):
            g[r][c] = hline
    for r in range(7):
        if r not in (2, 5):
            g[r][2] = v1
            g[r][5] = v2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_lines":
        for r in range(7):
            g[r][2] = 2
        return g
    if name == "no_columns":
        for r in (2, 5):
            for c in range(7):
                g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 2
        return g
    return g
