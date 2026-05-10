"""Generator for ef26cbf6.

Rule: blue cells in yellow-separated sections inherit marker colors
from paired sections.

Combinatorial axes (8): cell_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
n_markers.
Degenerates: no_separators, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c2478bfbf97e"
VERSION = "1.1.0"
TASK_ID = "c2478bfbf97e"
SUMMARY = "Blue cells in yellow sections inherit marker colors from paired sections."

INVARIANTS = [
    "yellow separator rows and columns divide the grid into equal sections",
    "some sections contain one non-blue non-yellow marker color",
    "blue cells in marker-free sections use a marker from same row or column",
    "marker colors are distinct from each other and from 0, 1, 4",
]

CELL_SIZES = ("c3", "c4")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separators", "no_markers", "full_grid")
HELPFUL_TEXTURES = CELL_SIZES

AXES = {
    "cell_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CELL_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "n_markers":      {"type": "int", "default": "2", "valid": "2"},
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
    if tx in CELL_SIZES:
        cell_size = int(tx[1])
    else:
        cell_size = ctx.draw_choice("cell_size", [3, 4])
    m1, m2 = ctx.draw_distinct_colors("markers", n=2, exclude={0, 1, 4})
    n = cell_size * 2 + 1
    g = full_grid(n, n, 0)
    sep = cell_size
    for i in range(n):
        g[sep][i] = 4
        g[i][sep] = 4
    g[1][1] = m1
    g[sep + 1][1] = m2
    for dr, dc in [(0, 0), (1, 1), (2, 0)]:
        if dr < cell_size and dc < cell_size:
            g[1 + dr][sep + 1 + dc] = 1
            g[sep + 1 + dr][sep + 1 + dc] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_separators":
        g[1][1] = 2
        return g
    if name == "no_markers":
        for i in range(7):
            g[3][i] = 4; g[i][3] = 4
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 4
        return g
    return g
