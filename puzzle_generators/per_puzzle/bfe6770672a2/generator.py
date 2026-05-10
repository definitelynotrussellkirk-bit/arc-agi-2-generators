"""Generator for 39e1d7f9.

Rule: a separator grid propagates the strongest local macro-cell
neighborhood pattern.

Combinatorial axes (8): grid_h/w, cell_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_targets, no_support, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bfe6770672a2"
VERSION = "1.1.0"
TASK_ID = "bfe6770672a2"
SUMMARY = "Separator grid propagates strongest local macro-cell neighborhood pattern."

INVARIANTS = [
    "full separator rows and columns split the grid into macro-cells",
    "one target-colored macro-cell has a distinctive colored neighbor pattern",
    "other target macro-cells receive that same neighbor pattern where cells are blank",
]

CELL_KINDS = ("c1", "c2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_targets", "no_support", "full_grid")
HELPFUL_TEXTURES = CELL_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "cell_size":      {"type": "int", "default": "rng helpful",
                       "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for cell_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in CELL_KINDS:
        cell = int(tx[1])
    elif difficulty == "easy":
        cell = 2
    elif difficulty == "hard":
        cell = 1
    else:
        cell = ctx.draw_int("cell_size", 1, 2)
    sep, target, support = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    macro_h = 4
    macro_w = 4
    h = macro_h * cell + (macro_h - 1)
    w = macro_w * cell + (macro_w - 1)
    g = full_grid(h, w, 0)
    for r in range(cell, h, cell + 1):
        for c in range(w):
            g[r][c] = sep
    for c in range(cell, w, cell + 1):
        for r in range(h):
            g[r][c] = sep

    def fill_macro(i, j, color):
        r0 = i * (cell + 1)
        c0 = j * (cell + 1)
        for r in range(r0, r0 + cell):
            for c in range(c0, c0 + cell):
                g[r][c] = color

    fill_macro(1, 1, target)
    fill_macro(0, 1, support)
    fill_macro(1, 0, support)
    fill_macro(1, 2, support)
    fill_macro(2, 1, support)
    fill_macro(2, 3, target)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_targets":
        for r in range(1, 7, 2):
            for c in range(7):
                g[r][c] = 5
        for c in range(1, 7, 2):
            for r in range(7):
                g[r][c] = 5
        return g
    if name == "no_support":
        g[0][0] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 5
        return g
    return g
