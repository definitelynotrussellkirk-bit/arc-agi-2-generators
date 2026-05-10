"""Generator for 045e512c.

Rule: central cross is replicated in the directions indicated by
colored markers.

Combinatorial axes (8): grid_size, n_markers, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
cross_color.
Degenerates: no_markers, no_cross, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b2d6e6b60917"
VERSION = "1.1.0"
TASK_ID = "b2d6e6b60917"
SUMMARY = "Central cross replicated in directions indicated by colored markers."

INVARIANTS = [
    "the cross is the largest object",
    "markers are single cells separated from the cross",
    "marker position relative to the cross selects the replication direction",
    "marker colors are distinct from each other and from the cross",
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
CROSS = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_cross", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 17..23", "valid": "12..30"},
    "n_markers":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "cross_color":    {"type": "color", "default": "rng !0", "valid": "1..9"},
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
    if difficulty == "easy":
        size_lo, size_hi, nm_lo, nm_hi = 17, 19, 1, 2
    elif difficulty == "hard":
        size_lo, size_hi, nm_lo, nm_hi = 23, 28, 4, 6
    else:
        size_lo, size_hi, nm_lo, nm_hi = 17, 23, 2, 4
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    n_markers = ctx.draw_int("n_markers", nm_lo, nm_hi)
    g = full_grid(size, size, 0)
    cr = cc = size // 2
    cross_color = ctx.draw_color("cross_color", exclude={0})
    for dr, dc in CROSS:
        g[cr + dr][cc + dc] = cross_color
    colors = list(ctx.draw_distinct_colors("marker_colors", n=n_markers, exclude={0, cross_color}))
    for (dr, dc), color in zip(rng.sample(DIRECTIONS, n_markers), colors):
        mr = cr + dr * 5
        mc = cc + dc * 5
        g[mr][mc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(20, 20, 0)
    if name == "no_markers":
        cr = cc = 10
        for dr, dc in CROSS:
            g[cr + dr][cc + dc] = 2
        return g
    if name == "no_cross":
        g[5][5] = 3
        g[15][15] = 4
        return g
    if name == "full_grid":
        for r in range(20):
            for c in range(20):
                g[r][c] = 2
        return g
    return g
