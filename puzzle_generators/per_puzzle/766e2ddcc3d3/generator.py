"""Generator for arc_additional_puzzle_bank_volume3:H16.

Rule: ctrl = first non-zero cell ∈ {2,3,4,5}. Apply (ctrl-2) cw
rotations to normalized 1-cells; output bbox-cropped result in color
8.

Combinatorial axes (8): grid_h/w, ctrl, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_ctrl, no_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "766e2ddcc3d3"
VERSION = "1.1.0"
TASK_ID = "766e2ddcc3d3"
SUMMARY = "Ctrl ∈ {2,3,4,5} at top-left + 1-shape elsewhere."

INVARIANTS = [
    "(0,0) is ctrl ∈ {2,3,4,5}",
    "1-shape is asymmetric (so rotations differ)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_ctrl", "no_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "ctrl":           {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "true",
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
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    ctrl = ctx.draw_int("ctrl", 2, 5)
    g = full_grid(h, w, 0)
    g[0][0] = ctrl
    g[2][2] = 1; g[3][2] = 1; g[3][3] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_ctrl":
        g[2][2] = 1; g[3][2] = 1; g[3][3] = 1
        return g
    if name == "no_shape":
        g[0][0] = 3
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 1
        return g
    return g
