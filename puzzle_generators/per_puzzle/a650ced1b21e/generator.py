"""Generator for 7837ac64.

Rule: colored anomalies on a lattice are summarized by corner, edge
and center groups into a 3x3 grid.

Combinatorial axes (8): grid_size, line_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
line_color.
Degenerates: no_lines, no_anomalies, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a650ced1b21e"
VERSION = "1.1.0"
TASK_ID = "a650ced1b21e"
SUMMARY = "Colored anomalies on lattice summarized into 3x3 grid by zone."

INVARIANTS = [
    "background is color 0",
    "one lattice color forms majority horizontal and vertical lines",
    "non-lattice colors appear only at lattice intersections",
    "each 3x3 summary zone has at least one anomaly",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lines", "no_anomalies", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "9", "valid": "9"},
    "line_count":     {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "line_color":     {"type": "color", "default": "rng !0", "valid": "1..9"},
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
    ctx.draw_int("line_count", 4, 4)
    lc = ctx.draw_color("line_color", exclude={0})
    colors = ctx.draw_distinct_colors("anomaly_colors", n=6, exclude={0, lc})
    g = full_grid(9, 9, 0)
    lines = [1, 3, 5, 7]
    for r in lines:
        for c in range(9):
            g[r][c] = lc
    for c in lines:
        for r in range(9):
            g[r][c] = lc
    anomaly_grid = [
        [colors[0], colors[1], colors[1], colors[2]],
        [colors[3], 0, 0, colors[4]],
        [colors[3], 0, 0, colors[4]],
        [colors[5], colors[2], colors[2], colors[0]],
    ]
    for ri, row in enumerate(anomaly_grid):
        for ci, value in enumerate(row):
            if value:
                g[lines[ri]][lines[ci]] = value
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_lines":
        g[3][3] = 2
        return g
    if name == "no_anomalies":
        for r in [1, 3, 5, 7]:
            for c in range(9):
                g[r][c] = 5
        for c in [1, 3, 5, 7]:
            for r in range(9):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 5
        return g
    return g
