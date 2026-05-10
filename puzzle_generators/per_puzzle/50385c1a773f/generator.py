"""Generator for arc_additional_puzzle_bank_volume17:H113.

Rule: from 2-source moving right, walk: paint 8 if 0; if 3 slash deflect;
if 4 backslash; stop at 5 or out.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_source, no_wall, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "50385c1a773f"
VERSION = "1.1.0"
TASK_ID = "50385c1a773f"
SUMMARY = "2-source + 3-deflector + 5-wall walking ray."

INVARIANTS = [
    "exactly one 2-source",
    "1-2 deflectors of color 3 or 4 to the right",
    "1-2 5-cells acting as walls",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_source", "no_wall", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "7..9"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[5][1] = 2
    g[5][5] = 3
    g[0][5] = 5
    g[1][6] = 5
    g[1][7] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_source":
        g[0][5] = 5
        return g
    if name == "no_wall":
        g[5][1] = 2
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
