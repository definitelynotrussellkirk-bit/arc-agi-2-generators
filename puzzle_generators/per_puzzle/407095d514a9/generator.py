"""Generator for fe9372f3.

Rule: red cross is kept while cardinal rays become 8/8/4 stripes and
diagonals become 1.

Combinatorial axes (8): grid_h/w, arm_length, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_cross, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "407095d514a9"
VERSION = "1.1.0"
TASK_ID = "407095d514a9"
SUMMARY = "Red cross kept; cardinal rays become 8/8/4 stripes and diagonals become 1."

INVARIANTS = [
    "background is color 0",
    "the source shape is made only of color-2 cells",
    "the mean of the red cells defines the ray center",
    "the cross sits clear of grid borders so all rays have room",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cross", "full_grid", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "arm_length":     {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
        arm_lo, arm_hi = 1, 1
    elif difficulty == "hard":
        arm_lo, arm_hi = 2, 2
    else:
        arm_lo, arm_hi = 1, 2
    arm = ctx.draw_int("arm_length", arm_lo, arm_hi)
    h = 9 + 2 * rng.randint(0, 2)
    w = 9 + 2 * rng.randint(0, 2)
    g = full_grid(h, w, 0)
    cr = h // 2
    cc = w // 2
    for d in range(-arm, arm + 1):
        g[cr + d][cc] = 2
        g[cr][cc + d] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_cross":
        return g
    if name == "single_cell":
        g[4][4] = 2
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 2
        return g
    return g
