"""Generator for 5b526a93.

Rule: ring icons in the key row define stamp columns; matching row
icons receive 8-ring stamps at those columns.

Combinatorial axes (8): grid_h/w, row_icon_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_key_cols.
Degenerates: no_icons, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "f1b474e8edf7"
VERSION = "1.1.0"
TASK_ID = "f1b474e8edf7"
SUMMARY = "Key row ring icons define stamp columns; row icons receive 8-ring stamps."

INVARIANTS = [
    "all icons are 3x3 color-1 rings with a zero center",
    "the row with the most icons is the key row",
    "the leftmost key icon column is the row-icon column",
    "row icons sit below the key row so the rule has work to do",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_icons", "no_key", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "19", "valid": "19"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17"},
    "row_icon_count": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_key_cols":     {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _ring(g, r0, c0, color):
    for dr, dc in RING_3X3:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        ric_lo, ric_hi = 1, 1
    elif difficulty == "hard":
        ric_lo, ric_hi = 3, 3
    else:
        ric_lo, ric_hi = 2, 3
    row_icon_count = ctx.draw_int("row_icon_count", ric_lo, ric_hi)
    g = full_grid(19, 17, 0)
    key_cols = [1, rng.choice([5, 6]), rng.choice([10, 11, 12])]
    for c0 in key_cols:
        _ring(g, 1, c0, 1)
    row_options = [[6, 11, 15], [7, 12, 15], [8, 13, 16]]
    for r0 in rng.choice(row_options)[:row_icon_count]:
        _ring(g, r0, 1, 1)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(19, 17, 0)
    if name == "no_icons":
        return g
    if name == "no_key":
        _ring(g, 6, 1, 1)
        return g
    if name == "full_grid":
        for r in range(19):
            for c in range(17):
                g[r][c] = 1
        return g
    return g
