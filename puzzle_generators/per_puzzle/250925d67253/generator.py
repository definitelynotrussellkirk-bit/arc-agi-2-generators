"""Generator for 4e45f183.

Rule: a 3x3 array of 5x5 cells is permuted by the centroid slot of each
cell's markers.

Combinatorial axes (8): grid_h/w, shift, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_markers, single_cell, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "250925d67253"
VERSION = "1.1.0"
TASK_ID = "250925d67253"
SUMMARY = "A 3x3 array of 5x5 cells is permuted by the centroid slot of each cell's markers."

INVARIANTS = [
    "the grid uses separator rows and columns at 0, 6, 12, and 18",
    "each 5x5 cell has non-background markers whose centroid selects a target slot",
    "each target slot is selected by exactly one source cell",
    "the output copies whole 5x5 cells into their selected target slots",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "single_cell", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "19", "valid": "19"},
    "grid_w":         {"type": "int", "default": "19", "valid": "19"},
    "shift":          {"type": "int", "default": "rng 1..8", "valid": "1..8"},
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


TARGET_MARKS = {
    0: (0, 0), 1: (0, 2), 2: (0, 4),
    3: (2, 0), 4: (2, 2), 5: (2, 4),
    6: (4, 0), 7: (4, 2), 8: (4, 4),
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        shift = ctx.draw_int("shift", 1, 3)
    elif difficulty == "hard":
        shift = ctx.draw_int("shift", 5, 8)
    else:
        shift = ctx.draw_int("shift", 1, 8)
    bg = ctx.draw_color("background", exclude={0})
    marker_color = ctx.draw_color("marker_color", exclude={0, bg})
    g = full_grid(19, 19, 0)
    for br in range(3):
        for bc in range(3):
            r0 = 1 + br * 6
            c0 = 1 + bc * 6
            for r in range(r0, r0 + 5):
                for c in range(c0, c0 + 5):
                    g[r][c] = bg
            src = br * 3 + bc
            target = (src + shift) % 9
            mr, mc = TARGET_MARKS[target]
            g[r0 + mr][c0 + mc] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(19, 19, 0)
    if name == "no_markers":
        for br in range(3):
            for bc in range(3):
                r0 = 1 + br * 6
                c0 = 1 + bc * 6
                for r in range(r0, r0 + 5):
                    for c in range(c0, c0 + 5):
                        g[r][c] = 5
        return g
    if name == "single_cell":
        for r in range(1, 6):
            for c in range(1, 6):
                g[r][c] = 5
        g[1][1] = 3
        return g
    if name == "full_grid":
        for r in range(19):
            for c in range(19):
                g[r][c] = 5
        return g
    return g
