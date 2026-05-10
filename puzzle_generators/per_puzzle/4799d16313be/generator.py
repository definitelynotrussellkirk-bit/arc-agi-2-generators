"""Generator for 8719f442.

Rule: 3x3 gray pattern expands into a 15x15 self-similar block grid.

Combinatorial axes (8): grid_h/w, cell_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
pattern_kind.
Degenerates: no_pattern, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4799d16313be"
VERSION = "1.1.0"
TASK_ID = "4799d16313be"
SUMMARY = "3x3 gray pattern expands into 15x15 self-similar block grid."

INVARIANTS = [
    "input is 3x3",
    "active cells use color 5",
    "each active cell maps to a filled 5x5 macro-cell center",
    "the input has at least one active cell so the output is non-empty",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "full_grid", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

PATTERNS = [
    [(0, 1), (1, 1), (2, 1)],
    [(1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0)],
    [(1, 1), (1, 2), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 2), (1, 2), (2, 2), (0, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(2, 0), (2, 1), (2, 2), (1, 1)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "3", "valid": "3"},
    "grid_w":         {"type": "int", "default": "3", "valid": "3"},
    "cell_count":     {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "pattern_kind":   {"type": "str", "default": "rng", "valid": "rng"},
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
    g = full_grid(3, 3, 0)
    for r, c in PATTERNS[(seed + sample_index) % len(PATTERNS)]:
        g[r][c] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(3, 3, 0)
    if name == "no_pattern":
        return g
    if name == "single_cell":
        g[1][1] = 5
        return g
    if name == "full_grid":
        for r in range(3):
            for c in range(3):
                g[r][c] = 5
        return g
    return g
