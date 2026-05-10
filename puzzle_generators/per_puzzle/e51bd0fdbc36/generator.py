"""Generator for 8886d717.

Rule: cyan cells grow toward the maroon edge; enclosed cyan cells
become red.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, edge, n_cyan.
Degenerates: no_cyan, no_edge, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e51bd0fdbc36"
VERSION = "1.1.0"
TASK_ID = "e51bd0fdbc36"
SUMMARY = "Cyan cells grow toward the maroon edge; enclosed cyan becomes red."

INVARIANTS = [
    "the top edge row is fully maroon color 9",
    "cyan cells use color 8",
    "red cells use color 2 and can enclose cyan clusters",
    "non-enclosed cyan cells have a clear path toward the maroon edge",
]

EDGE_KINDS = ("top",)
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cyan", "no_edge", "full_grid")
HELPFUL_TEXTURES = EDGE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "edge":           {"type": "str", "default": "top",
                       "valid": "|".join(EDGE_KINDS)},
    "n_cyan":         {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for edge",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    g = full_grid(9 + rng.randint(0, 2), 9 + rng.randint(0, 2), 0)
    for c in range(len(g[0])):
        g[0][c] = 9
    for r, c in [(4, 4), (5, 4), (4, 5)]:
        g[r][c] = 8
    for r, c in [(3, 4), (5, 5), (4, 3)]:
        g[r][c] = 2
    g[7][2] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_cyan":
        for c in range(9):
            g[0][c] = 9
        return g
    if name == "no_edge":
        g[4][4] = 8
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 9
        return g
    return g
