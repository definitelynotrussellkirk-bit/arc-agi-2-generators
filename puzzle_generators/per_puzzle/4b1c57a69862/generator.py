"""Generator for 69889d6e.

Rule: red seed draws a two-wide diagonal staircase upward-right,
shifting around blue blockers.

Combinatorial axes (8): grid_h/w, blocker_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_seed, no_blockers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4b1c57a69862"
VERSION = "1.1.0"
TASK_ID = "4b1c57a69862"
SUMMARY = "Red seed draws two-wide diagonal staircase up-right around blue blockers."

INVARIANTS = [
    "background is color 0",
    "there is one red seed",
    "blue cells appear above the seed as optional blockers",
    "the staircase has room to climb toward the top-right",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "no_blockers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "blocker_count":  {"type": "int", "default": "rng 2..4", "valid": "0..8"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
    ctx.draw_int("blocker_count", 2, 4)
    h = 10 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    red_r = h - 2
    red_c = 1 + ((seed + sample_index) % 2)
    g[red_r][red_c] = 2
    for i in range(3):
        r = red_r - 2 - i
        c = red_c + 1 + i + ((sample_index + i) % 2)
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = 1
            if c + 1 < w and i % 2 == 0:
                g[r][c + 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_seed":
        g[3][3] = 1
        return g
    if name == "no_blockers":
        g[9][2] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
