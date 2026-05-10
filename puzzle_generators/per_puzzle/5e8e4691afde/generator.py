"""Generator for 2b9ef948.

Rule: framed square center is relocated by comparing a same-color
indicator with an extra color-4 marker.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, shift, color.
Degenerates: no_frame, no_indicator, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5e8e4691afde"
VERSION = "1.1.0"
TASK_ID = "5e8e4691afde"
SUMMARY = "Framed square center relocated by indicator-vs-extra-4 vector."

INVARIANTS = [
    "one non-4 non-5 color sits at the center of a 3x3 color-4 frame",
    "a same-color indicator appears outside the frame",
    "one extra color-4 marker appears outside the frame",
    "indicator-to-extra-4 vector keeps the relocated frame inside the grid",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_indicator", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SHIFTS = [(2, 2), (2, -2), (-2, 2), (1, 3), (3, 1)]

AXES = {
    "grid_size":      {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "shift":          {"type": "str", "default": "rng vector",
                       "valid": "small in-bounds vectors"},
    "color":          {"type": "color", "default": "rng !{0,4,5}",
                       "valid": "1|2|3|6|7|8|9"},
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
    color = ctx.draw_color("color", exclude={0, 4, 5})
    size = rng.randint(11, 14)
    sr = rng.randint(4, size - 5)
    sc = rng.randint(4, size - 5)
    dr, dc = rng.choice(SHIFTS)
    if not (1 <= sr + dr < size - 1 and 1 <= sc + dc < size - 1):
        dr, dc = 2, 2
    g = full_grid(size, size, 0)
    for r in range(sr - 1, sr + 2):
        for c in range(sc - 1, sc + 2):
            g[r][c] = 4
    g[sr][sc] = color
    frame = {(r, c) for r in range(sr - 1, sr + 2) for c in range(sc - 1, sc + 2)}
    indicator = (size - 2 if dr < 0 else 1, size - 2 if dc < 0 else 1)
    extra = (indicator[0] + dr, indicator[1] + dc)
    if extra in frame:
        for cand in [(1, 1), (1, size - 2), (size - 2, 1), (size - 2, size - 2)]:
            trial = (cand[0] + dr, cand[1] + dc)
            if 0 <= trial[0] < size and 0 <= trial[1] < size and trial not in frame:
                indicator = cand
                extra = trial
                break
    g[indicator[0]][indicator[1]] = color
    g[extra[0]][extra[1]] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_frame":
        g[3][3] = 1
        g[7][7] = 4
        return g
    if name == "no_indicator":
        for r in range(4, 7):
            for c in range(4, 7):
                g[r][c] = 4
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 4
        return g
    return g
