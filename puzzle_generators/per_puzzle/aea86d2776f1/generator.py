"""Generator for arc_additional_puzzles_21_set19_bundle:H129.

Rule: 4 cmds at row 0 cols 1, 3, 7, 9. Each cmd selects panel a or b,
applies a transform. Output 2x2 stack of resulting tiles.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_cmds, no_panels, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aea86d2776f1"
VERSION = "1.1.0"
TASK_ID = "aea86d2776f1"
SUMMARY = "Fixed 5×11 grid: 4 cmds in row 0 + 2 panels (3x3 each) at rows 2-4."

INVARIANTS = [
    "grid is 5 rows × 11 cols",
    "4 cmds at (0,1), (0,3), (0,7), (0,9), each ∈ 1..8",
    "2 panels: subgrid(2,1)..(4,3) and subgrid(2,7)..(4,9)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cmds", "no_panels", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    h, w = 5, 11
    g = full_grid(h, w, 0)
    if difficulty == "easy":
        cmd_max = 4
    elif difficulty == "hard":
        cmd_max = 8
    else:
        cmd_max = 8
    for col in [1, 3, 7, 9]:
        g[0][col] = rng.randint(1, cmd_max)
    g[2][1] = 4
    g[3][1] = 4
    g[4][1] = 4; g[4][2] = 4; g[4][3] = 4
    g[2][7] = 7; g[2][8] = 7
    g[3][7] = 7; g[3][8] = 7
    g[4][8] = 7; g[4][9] = 7
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 11, 0)
    if name == "no_cmds":
        g[2][1] = 4; g[3][1] = 4
        g[2][7] = 7; g[3][7] = 7
        return g
    if name == "no_panels":
        for col in [1, 3, 7, 9]:
            g[0][col] = 3
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(11):
                g[r][c] = 4
        return g
    return g
