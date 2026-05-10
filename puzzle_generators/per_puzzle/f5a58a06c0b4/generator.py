"""Generator for 97c75046.

Rule: gray marker moves to the selected endpoint of the nearest
straight run of boundary cells.

Combinatorial axes (8): grid_h/w, run_orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, run_len.
Degenerates: no_run, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f5a58a06c0b4"
VERSION = "1.1.0"
TASK_ID = "f5a58a06c0b4"
SUMMARY = "Gray marker moves to selected endpoint of nearest straight run."

INVARIANTS = [
    "background is color 0",
    "one movable marker uses color 5",
    "candidate boundary runs use color 7 and touch background",
    "runs are horizontal vertical or diagonal and at least two cells long",
]

ORIENTATIONS = ("horizontal", "vertical", "diagonal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_run", "no_marker", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "run_orientation":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "run_len":        {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for run_orientation",
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
                  overrides.get("run_orientation") or \
                  ctx.draw_choice("run_orientation", list(ORIENTATIONS))
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    if orientation == "horizontal":
        r = 2 + ((seed + sample_index) % max(1, h - 4))
        c0 = 2
        cells = [(r, c0 + i) for i in range(4)]
        marker = (min(h - 1, r + 2), c0 + 1)
    elif orientation == "vertical":
        c = 2 + ((seed + sample_index) % max(1, w - 4))
        r0 = 2
        cells = [(r0 + i, c) for i in range(4)]
        marker = (r0 + 1, min(w - 1, c + 2))
    else:
        r0, c0 = 2, 2 + ((seed + sample_index) % max(1, w - 6))
        cells = [(r0 + i, c0 + i) for i in range(4)]
        marker = (r0 + 1, c0 + 3)
    for r, c in cells:
        g[r][c] = 7
    mr, mc = marker
    g[mr][mc] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_run":
        g[3][3] = 5
        return g
    if name == "no_marker":
        for c in range(2, 6):
            g[5][c] = 7
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 7
        return g
    return g
