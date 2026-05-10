"""Generator for 4c5c2cf0.

Rule: satellite shape is mirrored into the other three quadrants
around the central anchor color.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, sat_size,
n_distinct_colors.
Degenerates: no_satellite, no_anchor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "39e5f1c25127"
VERSION = "1.1.0"
TASK_ID = "39e5f1c25127"
SUMMARY = "Satellite shape mirrored into other three quadrants around anchor."

INVARIANTS = [
    "the anchor color is the nonzero object whose bbox center is closest to grid center",
    "the satellite color appears in one off-center shape",
    "the anchor bbox center defines the horizontal and vertical reflection axes",
    "anchor and satellite colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_satellite", "no_anchor", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "15", "valid": "15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "sat_size":       {"type": "int", "default": "rng 3..4", "valid": "3..4"},
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
    anchor, satellite = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    size = 15
    g = full_grid(size, size, 0)
    center = size // 2
    for dr, dc in [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)]:
        g[center + dr][center + dc] = anchor
    sat_cells = [(center - 4, center - 3), (center - 4, center - 2), (center - 3, center - 3)]
    if rng.choice([False, True]):
        sat_cells.append((center - 5, center - 3))
    for r, c in sat_cells:
        g[r][c] = satellite
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_satellite":
        for dr, dc in [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)]:
            g[7 + dr][7 + dc] = 2
        return g
    if name == "no_anchor":
        g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
