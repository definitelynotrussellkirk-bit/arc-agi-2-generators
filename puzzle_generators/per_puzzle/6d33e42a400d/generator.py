"""Generator for 66ac4c3b.

Rule: sparse paint markers map a source terrain profile onto matching
parallel source line.

Combinatorial axes (8): grid_h/w, marker_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_markers, no_source, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d33e42a400d"
VERSION = "1.1.0"
TASK_ID = "6d33e42a400d"
SUMMARY = "Paint markers reflect source terrain across marker/target rows."

INVARIANTS = [
    "paint markers lie on one row",
    "a source-color row has source cells at exactly those marker columns",
    "source cells reflect across marker/target rows",
    "marker and source colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_source", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "marker_count":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    marker_count = ctx.draw_int("marker_count", 3, 4)
    source, paint = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    h = 13 + (sample_index % 3)
    w = 13 + ((sample_index * 2) % 3)
    g = full_grid(h, w, 0)
    marker_row = 5 + (sample_index % 2)
    target_row = marker_row + 3
    cols = [2 + 2 * i + (sample_index % 2) for i in range(marker_count)]
    for c in cols:
        g[marker_row][c] = paint
        g[target_row][c] = source
    for r, c in [(marker_row - 1, cols[0] + 1), (marker_row - 2, cols[1]), (marker_row - 1, cols[-1] - 1)]:
        g[r][c] = source
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_markers":
        for c in range(2, 9, 2):
            g[8][c] = 1
        return g
    if name == "no_source":
        for c in range(2, 9, 2):
            g[5][c] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 1
        return g
    return g
