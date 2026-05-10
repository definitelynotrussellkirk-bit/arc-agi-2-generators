"""Generator for arc_additional_puzzles_21_set9:M62 — Two-panel boolean by code.

Rule: code at (0,0) ∈ {1,2,else}; 5-divider col splits 2 panels. For each
cell, code 1 = OR, code 2 = AND, else = XOR. Output single panel of 7s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, no_divider, identical_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3c66fa1a10c7"
VERSION = "1.1.0"
TASK_ID = "3c66fa1a10c7"
SUMMARY = "Code at (0,0) + 2 panels separated by 5-divider; each cell has random non-zero or zero."

INVARIANTS = [
    "code at (0,0) ∈ {1, 2, 3}",
    "5-divider in middle column",
    "each panel has 1-3 non-zero cells in similar positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "no_divider", "identical_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..5", "valid": "4..6"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "9..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code":           {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "panel_w":        {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "n_rows":         {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "code_plus_two_panels",
                       "valid": "code_plus_two_panels"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
        code = ctx.draw_int("code", 1, 1)
        pw = ctx.draw_int("panel_w", 4, 4)
        body_h = ctx.draw_int("n_rows", 3, 3)
    elif difficulty == "hard":
        code = ctx.draw_int("code", 2, 3)
        pw = ctx.draw_int("panel_w", 5, 5)
        body_h = ctx.draw_int("n_rows", 4, 4)
    else:
        code = ctx.draw_int("code", 1, 3)
        pw = ctx.draw_int("panel_w", 4, 5)
        body_h = ctx.draw_int("n_rows", 3, 4)
    h = body_h + 1
    w = pw * 2 + 1
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = code
    div = pw
    for r in range(1, h):
        g[r][div] = 5
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    for r in range(1, h):
        for c in range(pw):
            if rng.random() < 0.5:
                g[r][c] = color
            if rng.random() < 0.5:
                g[r][div + 1 + c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w, pw = 4, 9, 4
    g = full_grid(h, w, 0)
    div = pw
    if name == "no_code":
        # panels with divider but (0,0) is 0 → no boolean operation specified
        for r in range(1, h):
            g[r][div] = 5
        g[1][1] = 4; g[2][2] = 4
        g[1][6] = 4; g[3][7] = 4
        return g
    if name == "no_divider":
        # code present but no 5-divider → no panel boundary defined
        g[0][0] = 1
        g[1][1] = 4
        g[2][6] = 4
        return g
    if name == "identical_panels":
        # both panels identical → AND/OR/XOR all give same result (no signal)
        g[0][0] = 1
        for r in range(1, h):
            g[r][div] = 5
        for r, c in [(1, 1), (2, 2), (3, 1)]:
            g[r][c] = 4
            g[r][div + 1 + c] = 4
        return g
    return g
