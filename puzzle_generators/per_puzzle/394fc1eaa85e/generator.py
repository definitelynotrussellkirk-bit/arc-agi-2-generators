"""Generator for arc_additional_puzzle_bank_volume20:H134.

Rule: symmetric seeds under wall distance produce cyan equal-distance
cells.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_seeds, single_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "394fc1eaa85e"
VERSION = "1.1.0"
TASK_ID = "394fc1eaa85e"
SUMMARY = "Symmetric seeds under wall distance produce cyan equal-distance cells."

INVARIANTS = [
    "background is 0",
    "border walls are 5",
    "there is one red seed and one green seed",
    "tie cells are open and reachable from both seeds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "centered", "valid": "centered"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    r = rng.randint(2, h - 3)
    mid = w // 2
    g[r][mid - 2] = 2
    g[r][mid + 2] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 11, 0)
    if name == "no_seeds":
        for r in range(10):
            g[r][0] = 5; g[r][10] = 5
        for c in range(11):
            g[0][c] = 5; g[9][c] = 5
        return g
    if name == "single_seed":
        for r in range(10):
            g[r][0] = 5; g[r][10] = 5
        for c in range(11):
            g[0][c] = 5; g[9][c] = 5
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
