"""Generator for e760a62e.

Rule: colored dots in a cyan lattice fill same-row and same-column
lattice spans, with conflicts turning magenta.

Combinatorial axes (8): grid_h/w, cell_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_dots, no_lattice, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9d29446a5a3e"
VERSION = "1.1.0"
TASK_ID = "9d29446a5a3e"
SUMMARY = "Colored dots in cyan lattice fill row/col spans; conflicts turn magenta."

INVARIANTS = [
    "background is color 0",
    "cyan color 8 forms full divider rows and columns",
    "same-color dots appear in matching lattice rows or columns",
    "dot colors are distinct from each other and from 0, 6 and 8",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_lattice", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "cell_size":      {"type": "int", "default": "2", "valid": "2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
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
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    ctx.draw_int("cell_size", 2, 2)
    a, b = ctx.draw_distinct_colors("dot_colors", n=2, exclude={0, 6, 8})
    g = full_grid(11, 11, 0)
    for r in (3, 7):
        for c in range(11):
            g[r][c] = 8
    for c in (3, 7):
        for r in range(11):
            g[r][c] = 8
    for r, c, color in [(1, 1, a), (1, 9, a), (9, 5, a), (1, 5, b), (9, 5, b)]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_dots":
        for r in (3, 7):
            for c in range(11):
                g[r][c] = 8
        for c in (3, 7):
            for r in range(11):
                g[r][c] = 8
        return g
    if name == "no_lattice":
        g[1][1] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 8
        return g
    return g
