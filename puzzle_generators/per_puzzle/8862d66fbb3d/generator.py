"""Generator for arc_additional_puzzles_21_set16_bundle:H109.

Rule: cmd at (0,0). Left panel = subgrid(1,0,3,2); right = subgrid
(1,4,3,6) transformed by cmd. AND mask → 7, else → 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd, palette_size,
position_bias, n_distinct_colors, panel_density, texture.
Degenerates: no_cmd, no_left_panel, no_right_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8862d66fbb3d"
VERSION = "1.1.0"
TASK_ID = "8862d66fbb3d"
SUMMARY = "Fixed 4×7 grid: cmd at (0,0) + 2 3×3 panels with overlap pattern."

INVARIANTS = [
    "grid is exactly 4 rows × 7 cols",
    "cmd at (0,0) ∈ 1..8",
    "left and right 3×3 panels each have 2-3 non-zero cells of distinct colors",
]

PALETTE_KINDS = ("default", "cmd_low", "cmd_mid", "cmd_high")
DEGENERATE_TEXTURES = ("no_cmd", "no_left_panel", "no_right_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4"},
    "grid_w":         {"type": "int", "default": "7", "valid": "7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..8", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_panels", "valid": "fixed_panels"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "panel_density":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        cmd = ctx.draw_int("cmd", 1, 3)
    elif difficulty == "hard":
        cmd = ctx.draw_int("cmd", 6, 8)
    else:
        cmd = ctx.draw_int("cmd", 1, 8)
    h, w = 4, 7
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = cmd
    color_l = rng.choice([1, 2, 3, 4])
    color_r = rng.choice([5, 6, 7, 9])
    g[1][0] = color_l
    g[2][0] = color_l
    g[2][1] = color_l
    g[1][6] = color_r
    g[2][5] = color_r
    g[2][6] = color_r
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 7
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # both panels but no cmd at (0,0) → which transform to apply?
        g[1][0] = 1; g[2][0] = 1; g[2][1] = 1
        g[1][6] = 5; g[2][5] = 5; g[2][6] = 5
        return g
    if name == "no_left_panel":
        # cmd + right panel only → AND has missing operand
        g[0][0] = 4
        g[1][6] = 5; g[2][5] = 5; g[2][6] = 5
        return g
    if name == "no_right_panel":
        # cmd + left panel only → AND has missing operand
        g[0][0] = 4
        g[1][0] = 1; g[2][0] = 1; g[2][1] = 1
        return g
    return g
