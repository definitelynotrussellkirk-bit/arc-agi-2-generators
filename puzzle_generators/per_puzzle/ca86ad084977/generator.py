"""Generator for arc_additional_puzzle_bank_volume10:H65.

Rule: a single corridor routes ordered checkpoints 2 to 3 to 4 to 7.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_corridor, no_checkpoints, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ca86ad084977"
VERSION = "1.1.0"
TASK_ID = "ca86ad084977"
SUMMARY = "A single corridor routes ordered checkpoints 2 to 3 to 4 to 7."

INVARIANTS = [
    "walls are 5",
    "one row corridor is open",
    "checkpoints appear in order along the corridor",
    "each segment has a unique shortest path",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_corridor", "no_checkpoints", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 13, 18)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 5)
    r = rng.randint(1, h - 2)
    c0 = rng.randint(1, w - 11)
    checkpoints = [(c0, 2), (c0 + 3, 3), (c0 + 6, 4), (c0 + 9, 7)]
    for c in range(c0, c0 + 10):
        g[r][c] = 0
    for c, color in checkpoints:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 14, 5)
    if name == "no_corridor":
        return g
    if name == "no_checkpoints":
        for c in range(2, 12):
            g[3][c] = 0
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(14):
                g[r][c] = 0
        return g
    return g
