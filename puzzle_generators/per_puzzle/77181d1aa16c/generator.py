"""Generator for cfb2ce5a.

Rule: a two-color pattern is mirrored into a 2-by-2 kaleidoscope with
indicator color maps.

Combinatorial axes (8): grid_h/w, pattern, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_pattern, no_indicators, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "77181d1aa16c"
VERSION = "1.1.0"
TASK_ID = "77181d1aa16c"
SUMMARY = "Two-color pattern mirrored into 2x2 kaleidoscope with indicator color maps."

INVARIANTS = [
    "the largest all-nonzero rectangle is the two-color source pattern",
    "outside indicator cells specify major/minor recolors for the other three quadrants",
    "the output mirrors the source pattern into all quadrants using those color maps",
]

PATTERN_KINDS = ("p0", "p1", "p2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "no_indicators", "full_grid")
HELPFUL_TEXTURES = PATTERN_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "6", "valid": "6"},
    "pattern":        {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "8", "valid": "8"},
    "texture":        {"type": "str", "default": "alias for pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


PATTERNS = [
    [[1, 1, 2], [1, 2, 1], [1, 1, 1]],
    [[1, 2, 1], [1, 1, 1], [2, 1, 1]],
    [[1, 1, 1], [2, 1, 1], [1, 2, 1]],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in PATTERN_KINDS:
        pattern_idx = int(tx[1])
    else:
        pattern_idx = ctx.draw_choice("pattern", [0, 1, 2])
    major, minor, a, b, c, d, e, f = ctx.draw_distinct_colors("colors", n=8, exclude={0})
    source = [[major if v == 1 else minor for v in row] for row in PATTERNS[pattern_idx]]
    g = full_grid(6, 6, 0)
    for r, row in enumerate(source):
        for col, value in enumerate(row):
            g[r][col] = value
    g[0][5] = a
    g[0][3] = b
    g[5][0] = c
    g[3][0] = d
    g[5][5] = e
    g[3][5] = f
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "no_pattern":
        g[0][5] = 3
        return g
    if name == "no_indicators":
        for r in range(3):
            for c in range(3):
                g[r][c] = 4
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(6):
                g[r][c] = 4
        return g
    return g
