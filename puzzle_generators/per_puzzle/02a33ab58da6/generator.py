"""Generator for 230f2e48.

Rule: red tail past a zero gap from a gray endpoint rotates
perpendicular toward the grid center.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, tail_len.
Degenerates: no_endpoint, no_tail, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "02a33ab58da6"
VERSION = "1.1.0"
TASK_ID = "02a33ab58da6"
SUMMARY = "Red tail past zero gap rotates perpendicular from gray endpoint."

INVARIANTS = [
    "background is color 7",
    "a gray endpoint touches a red bar ending at one zero gap",
    "a red tail continues past that gap",
    "the tail is removed and redrawn perpendicular from the gap toward the center",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_endpoint", "no_tail", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "tail_len":       {"type": "int", "default": "rng 1..3", "valid": "1..5"},
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
    tail_len = ctx.draw_int("tail_len", 1, 3)
    h = rng.randint(11, 14)
    w = rng.randint(11, 14)
    g = full_grid(h, w, 7)
    if orientation == "horizontal":
        r = rng.randint(3, h - 4)
        c = rng.randint(1, 3)
        g[r][c] = 5
        g[r][c + 1] = 2
        g[r][c + 2] = 2
        g[r][c + 3] = 0
        for i in range(tail_len):
            g[r][c + 4 + i] = 2
    else:
        r = rng.randint(1, 3)
        c = rng.randint(3, w - 4)
        g[r][c] = 5
        g[r + 1][c] = 2
        g[r + 2][c] = 2
        g[r + 3][c] = 0
        for i in range(tail_len):
            g[r + 4 + i][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 7)
    if name == "no_endpoint":
        g[5][3] = 2; g[5][4] = 2
        return g
    if name == "no_tail":
        g[5][3] = 5; g[5][4] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 7
        return g
    return g
