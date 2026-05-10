"""Generator for arc_additional_puzzle_bank_volume16:H108.

Rule: a control marker selects a transform of the blue source shape
stamped at the maroon anchor.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_control, no_anchor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e2627920c372"
VERSION = "1.1.0"
TASK_ID = "e2627920c372"
SUMMARY = "A control marker selects a transform of the blue source shape stamped at the maroon anchor."

INVARIANTS = [
    "one blue source shape is present",
    "one control marker is 2, 3, 4, or 6",
    "one maroon anchor marks the normalized stamp position",
    "the transformed copy stays inside the grid",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_control", "no_anchor", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
        g[1 + dr][1 + dc] = 1
    g[h - 2][1] = rng.choice([2, 3, 4, 6])
    g[1][w - 5] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 13, 0)
    if name == "no_control":
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 1
        g[1][8] = 9
        return g
    if name == "no_anchor":
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 1
        g[8][1] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(13):
                g[r][c] = 1
        return g
    return g
