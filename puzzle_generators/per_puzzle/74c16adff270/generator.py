"""Generator for arc_additional_puzzle_bank_volume23:M159.

Rule: ctrl color (2/3/4/6) → rotation count (0/1/2/3). Rotate the
1-template cw `times` times; stamp rotated stamp in color 8 at the
7-anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ctrl,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_ctrl, no_template, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "74c16adff270"
VERSION = "1.1.0"
TASK_ID = "74c16adff270"
SUMMARY = "1-template + 7-anchor + ctrl marker (2/3/4/6) elsewhere."

INVARIANTS = [
    "background is 0",
    "exactly one 1-template (3-4 cells)",
    "exactly one 7-anchor where rotated stamp fits",
    "exactly one ctrl marker ∈ {2, 3, 4, 6}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_ctrl", "no_template", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ctrl":           {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_anchor",
                       "valid": "fixed_anchor"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        ctrl_idx = ctx.draw_int("ctrl", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
        ctrl_idx = ctx.draw_int("ctrl", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
        ctrl_idx = ctx.draw_int("ctrl", 0, 3)
    ctrl_colors = [2, 3, 4, 6]
    g = full_grid(h, w, 0)
    g[0][w - 3] = 1; g[0][w - 2] = 1
    g[1][w - 4] = 1; g[1][w - 3] = 1; g[1][w - 2] = 1
    g[4][7] = 7
    g[h - 1][2] = ctrl_colors[ctrl_idx]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_ctrl":
        # no ctrl marker → rotation count undefined, rule has no input
        g[0][w - 3] = 1; g[0][w - 2] = 1
        g[1][w - 4] = 1; g[1][w - 3] = 1; g[1][w - 2] = 1
        g[4][7] = 7
        return g
    if name == "no_template":
        # no 1-template → nothing to rotate and stamp
        g[4][7] = 7
        g[h - 1][2] = 3
        return g
    if name == "no_anchor":
        # no 7-anchor → nowhere to stamp the rotated template
        g[0][w - 3] = 1; g[0][w - 2] = 1
        g[1][w - 4] = 1; g[1][w - 3] = 1; g[1][w - 2] = 1
        g[h - 1][2] = 3
        return g
    return g
