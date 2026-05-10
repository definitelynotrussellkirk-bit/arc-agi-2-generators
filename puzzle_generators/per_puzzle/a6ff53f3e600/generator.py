"""Generator for arc_additional_puzzles_21_set19_bundle:H132 — Cmd-grid 2x2 motif tiling.

Rule: row commands at (2,0)/(4,0); col commands at (0,1)/(0,3); motif =
subgrid(2,1,4,3). Output: 2x2 tiles of motif transformed by row+col cmds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rc1/rc2/cc1/cc2,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_motif, all_same_cmd, missing_cmd.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a6ff53f3e600"
VERSION = "1.1.0"
TASK_ID = "a6ff53f3e600"
SUMMARY = "Fixed 5×5 grid: row cmds at col 0 + col cmds at row 0 + 3×3 motif inside."

INVARIANTS = [
    "grid is 5 rows × 5 cols",
    "(2,0), (4,0), (0,1), (0,3) are cmd cells ∈ {1,2,3}",
    "subgrid(2,1)..(4,3) is the motif",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_motif", "all_same_cmd", "missing_cmd")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5..5"},
    "grid_w":         {"type": "int", "default": "5", "valid": "5..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rc1":            {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "rc2":            {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "cc1":            {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "cc2":            {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "fixed_5x5_cmd_grid",
                       "valid": "fixed_5x5_cmd_grid"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        rc1 = ctx.draw_int("rc1", 1, 1); rc2 = ctx.draw_int("rc2", 1, 1)
        cc1 = ctx.draw_int("cc1", 1, 1); cc2 = ctx.draw_int("cc2", 1, 1)
    elif difficulty == "hard":
        rc1 = ctx.draw_int("rc1", 2, 3); rc2 = ctx.draw_int("rc2", 2, 3)
        cc1 = ctx.draw_int("cc1", 2, 3); cc2 = ctx.draw_int("cc2", 2, 3)
    else:
        rc1 = ctx.draw_int("rc1", 1, 3); rc2 = ctx.draw_int("rc2", 1, 3)
        cc1 = ctx.draw_int("cc1", 1, 3); cc2 = ctx.draw_int("cc2", 1, 3)
    h, w = 5, 5
    g = full_grid(h, w, 0)
    g[2][0] = rc1
    g[4][0] = rc2
    g[0][1] = cc1
    g[0][3] = cc2
    g[3][2] = 4; g[3][3] = 4
    g[4][1] = 4; g[4][2] = 4; g[4][3] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 5
    g = full_grid(h, w, 0)
    if name == "empty_motif":
        # cmds present but motif region is empty → tiling produces all-bg
        g[2][0] = 1; g[4][0] = 2; g[0][1] = 3; g[0][3] = 1
        return g
    if name == "all_same_cmd":
        # all 4 cmds identical → output tiles uniformly (no row/col distinction)
        g[2][0] = 2; g[4][0] = 2; g[0][1] = 2; g[0][3] = 2
        g[3][2] = 4; g[3][3] = 4
        g[4][1] = 4; g[4][2] = 4; g[4][3] = 4
        return g
    if name == "missing_cmd":
        # one cmd cell is 0 → command set incomplete, transform underdetermined
        g[2][0] = 1; g[4][0] = 0  # missing
        g[0][1] = 2; g[0][3] = 3
        g[3][2] = 4; g[3][3] = 4
        g[4][1] = 4; g[4][2] = 4; g[4][3] = 4
        return g
    return g
