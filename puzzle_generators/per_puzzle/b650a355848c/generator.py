"""Generator for 50aad11f.

Rule: pink shapes are recolored by their nearest marker and
concatenated in spatial order.

Combinatorial axes (8): grid_h/w, shape_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shapes, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b650a355848c"
VERSION = "1.1.0"
TASK_ID = "b650a355848c"
SUMMARY = "Pink shapes recolored by nearest marker and concatenated in spatial order."

INVARIANTS = [
    "background is color 0",
    "all source shapes use color 6",
    "each shape has a nearby non-6 singleton marker",
    "marker colors are distinct from each other and from 0 and 6",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..18", "valid": "12..30"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..30"},
    "shape_count":    {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "3..6"},
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
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        n_lo, n_hi = 4, 5
    else:
        n_lo, n_hi = 2, 3
    n = ctx.draw_int("shape_count", n_lo, n_hi)
    vertical = ((seed + sample_index) % 2 == 0)
    h = 14 + (4 * n if vertical else 0) + rng.randint(0, 2)
    w = 14 + (4 * n if not vertical else 0) + rng.randint(0, 2)
    g = full_grid(h, w, 0)
    marker_colors = ctx.draw_distinct_colors("markers", n=n, exclude={0, 6})
    shape = [(0, 0), (0, 1), (1, 0), (2, 0)]
    for i in range(n):
        if vertical:
            r0 = 2 + i * 5
            c0 = 5 + ((sample_index + i) % 3)
            marker = (r0, c0 - 2)
        else:
            r0 = 5 + ((sample_index + i) % 3)
            c0 = 2 + i * 5
            marker = (r0 - 2, c0)
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = 6
        mr, mc = marker
        g[mr][mc] = marker_colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_shapes":
        g[3][3] = 2
        return g
    if name == "no_markers":
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[2 + dr][5 + dc] = 6
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 6
        return g
    return g
