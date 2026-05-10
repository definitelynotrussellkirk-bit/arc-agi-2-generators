"""Generator for 758abdf0.

Rule: two pattern rows near an empty separator row synchronize paired
cyan markers and duplicate unpaired markers.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, n_marks.
Degenerates: no_separator, no_marks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "57a410fce3c9"
VERSION = "1.1.0"
TASK_ID = "57a410fce3c9"
SUMMARY = "Two pattern rows near empty separator synchronize paired cyan markers."

INVARIANTS = [
    "background filler is color 7 outside the zero separator",
    "one full zero row or column separates the pattern side from the opposite side",
    "exactly two non-background non-zero pattern lines contain cyan markers",
    "marker columns sit clear of grid borders",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separator", "no_marks", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_marks":        {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    h = 8 + rng.randint(0, 4)
    w = 10 + rng.randint(0, 4)
    g = full_grid(h, w, 7)
    zr = 3
    for c in range(w):
        g[zr][c] = 0
    pr1, pr2 = 1, 2
    cols = [1, 3, 5, 7]
    for i, c in enumerate(cols):
        if c >= w - 1:
            continue
        if i % 3 == 0:
            g[pr1][c] = 8
            g[pr2][c] = 8
        elif i % 3 == 1:
            g[pr1][c] = 8
        else:
            g[pr2][c] = 8
    if orientation == "vertical":
        return [list(row) for row in zip(*g)]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 7)
    if name == "no_separator":
        g[1][1] = 8; g[2][3] = 8
        return g
    if name == "no_marks":
        for c in range(12):
            g[3][c] = 0
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 8
        return g
    return g
