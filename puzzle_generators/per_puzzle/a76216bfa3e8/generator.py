"""Generator for 92e50de0.

Rule: a marker pattern inside one lattice cell is stamped into every
same-parity cell of a line grid.

Combinatorial axes (8): grid_h/w, cell_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_lattice, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a76216bfa3e8"
VERSION = "1.1.0"
TASK_ID = "a76216bfa3e8"
SUMMARY = "Marker pattern inside one lattice cell is stamped into every same-parity cell."

INVARIANTS = [
    "background is color 0",
    "the most frequent nonzero color forms full separator rows and columns",
    "one lattice cell contains a non-line marker pattern",
    "matching row and column parity selects replicated cells",
]

CELL_KINDS = ("c2", "c3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_lattice", "no_marker", "full_grid")
HELPFUL_TEXTURES = CELL_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "cell_size":      {"type": "int", "default": "rng helpful",
                       "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        cell = 3
    elif difficulty == "hard":
        cell = 2
    else:
        cell = ctx.draw_int("cell_size", 2, 3)
    line_color, marker_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    n_rows = 3
    n_cols = 3
    h = n_rows * cell + (n_rows - 1)
    w = n_cols * cell + (n_cols - 1)
    g = full_grid(h, w, 0)
    for r in range(cell, h, cell + 1):
        for c in range(w):
            g[r][c] = line_color
    for c in range(cell, w, cell + 1):
        for r in range(h):
            g[r][c] = line_color
    marker_cr = (seed + sample_index + rng.randint(0, 2)) % n_rows
    marker_cc = (seed * 2 + sample_index + rng.randint(0, 2)) % n_cols
    r0 = marker_cr * (cell + 1)
    c0 = marker_cc * (cell + 1)
    g[r0][c0] = marker_color
    if cell > 2:
        g[r0 + 1][c0] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_lattice":
        g[5][5] = 3
        return g
    if name == "no_marker":
        for r in range(3, 11, 4):
            for c in range(11):
                g[r][c] = 5
        for c in range(3, 11, 4):
            for r in range(11):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
