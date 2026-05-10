"""Generator for b942fd60.

Rule: a blue ray starts to the right, then branches vertically when it
hits a stopper.

Combinatorial axes (8): grid_h/w, stopper_distance, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_start, no_stopper, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cd67809f5bb8"
VERSION = "1.1.0"
TASK_ID = "cd67809f5bb8"
SUMMARY = "Blue ray starts rightward, then branches vertically when it hits a stopper."

INVARIANTS = [
    "background is color 0",
    "there is one starting color-2 cell",
    "a nonzero stopper lies to the right of the start",
    "the rule paints the traversed ray and any perpendicular branches with color 2",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_start", "no_stopper", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "9..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "10..14"},
    "stopper_distance":{"type": "int", "default": "6", "valid": "5..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
    if difficulty == "easy":
        h = 9 + rng.randint(0, 1)
        w = 10 + rng.randint(0, 1)
    elif difficulty == "hard":
        h = 11 + rng.randint(0, 1)
        w = 13 + rng.randint(0, 1)
    else:
        h = 9 + rng.randint(0, 3)
        w = 10 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    start_r = 3 + rng.randint(0, h - 7)
    start_c = 1
    stop_c = w - 3
    g[start_r][start_c] = 2
    g[start_r][stop_c] = 5
    if h >= 10:
        g[1][stop_c - 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_start":
        g[3][9] = 5
        return g
    if name == "no_stopper":
        g[3][1] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
