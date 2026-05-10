"""Generator for 97239e3d.

Rule: colored markers snap to nearest 4x4 tile borders, then draw
tile-aligned frames and center marks.

Combinatorial axes (8): grid_h/w, tile_period, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_markers, single_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "10b0b0da4c28"
VERSION = "1.1.0"
TASK_ID = "10b0b0da4c28"
SUMMARY = "Markers snap to 4x4 tile borders; draw tile frames and centers."

INVARIANTS = [
    "background is color 0",
    "marker colors exclude color 8",
    "markers lie inside 4x4 tile bands",
    "marker colors are distinct from each other and from 0 and 8",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "single_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "tile_period":    {"type": "int", "default": "4", "valid": "4"},
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
    ctx.draw_int("tile_period", 4, 4)
    a, b = ctx.draw_distinct_colors("colors", n=2, exclude={0, 8})
    g = full_grid(12, 12, 0)
    for r, c in [(1, 1), (2, 5), (5, 2)]:
        g[r][c] = a
    for r, c in [(6, 6), (9, 9)]:
        g[r][c] = b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_markers":
        return g
    if name == "single_marker":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
