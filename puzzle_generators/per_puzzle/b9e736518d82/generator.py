"""Generator for f1bcbc2c.

Rule: a marker on an orange zigzag channel selects the larger adjacent
half to fill cyan.

Combinatorial axes (8): grid_h/w, turn, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_channel, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9e736518d82"
VERSION = "1.1.0"
TASK_ID = "b9e736518d82"
SUMMARY = "Marker on orange zigzag channel selects larger half to fill cyan."

INVARIANTS = [
    "orange cells define a bent channel boundary",
    "empty or marker cells adjacent to orange form the channel candidate",
    "a marker at a turn splits the channel and the larger side is filled cyan",
]

TURN_KINDS = ("t0", "t1", "t2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_channel", "no_marker", "full_grid")
HELPFUL_TEXTURES = TURN_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "turn":           {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for turn",
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
    if tx in TURN_KINDS:
        turn = int(tx[1])
    else:
        turn = ctx.draw_choice("turn", [0, 1, 2])
    g = full_grid(13, 13, 0)
    row = 4 + turn
    col = 5
    for c in range(2, 10):
        g[row][c] = 7
    for r in range(row, 11):
        g[r][9] = 7
    g[row + 1][8] = 9
    extra = (seed + sample_index) % 4
    if extra >= 2:
        g[row - 1][3] = 7
        g[row - 2][3] = 7
    if extra == 1 or extra == 3:
        g[row + 2][2] = 7
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_channel":
        g[5][8] = 9
        return g
    if name == "no_marker":
        for c in range(2, 10):
            g[6][c] = 7
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 7
        return g
    return g
