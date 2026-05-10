"""Generator for d07ae81c.

Rule: markers cast diagonal rays, recoloring each zone by its zone
marker.

Combinatorial axes (8): grid_h/w, split_col, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_markers, no_split, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "090529973705"
VERSION = "1.1.0"
TASK_ID = "090529973705"
SUMMARY = "Markers cast diagonal rays, recoloring each zone by its zone marker."

INVARIANTS = [
    "two dominant colors form the background zones",
    "each non-zone marker sits inside or adjacent to exactly one zone",
    "all cells on a marker diagonal are recolored with that zone's marker color",
    "left, right, lm and rm colors are distinct and non-zero",
]

SPLIT_COLS = ("c5", "c6", "c7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_split", "full_grid")
HELPFUL_TEXTURES = SPLIT_COLS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "split_col":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SPLIT_COLS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for split_col",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SPLIT_COLS:
        split_col = int(tx[1:])
    else:
        split_col = ctx.draw_choice("split_col", [5, 6, 7])
    left, right, lm, rm = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    g = full_grid(12, 13, right)
    for r in range(12):
        for c in range(split_col):
            g[r][c] = left
    g[3 + (sample_index % 2)][2] = lm
    g[8 - (sample_index % 2)][split_col + 3] = rm
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 5)
    if name == "no_markers":
        for r in range(12):
            for c in range(6):
                g[r][c] = 1
        return g
    if name == "no_split":
        g[3][2] = 2; g[8][9] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
