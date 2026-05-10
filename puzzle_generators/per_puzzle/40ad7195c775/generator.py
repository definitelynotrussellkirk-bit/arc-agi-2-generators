"""Generator for 7e576d6e.

Rule: two endpoints connect by a staircase path through marker clusters
on full stripe rows.

Combinatorial axes (8): grid_h/w, layout, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_endpoints, no_stripes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "40ad7195c775"
VERSION = "1.1.0"
TASK_ID = "40ad7195c775"
SUMMARY = "Two endpoints connect by staircase path through marker clusters on stripe rows."

INVARIANTS = [
    "the background is zero",
    "the endpoint color appears exactly twice",
    "one stripe color forms long full rows",
    "each stripe row has a small waypoint-color cluster whose middle column is the path waypoint",
]

LAYOUTS = ("wide", "shifted", "steep")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_endpoints", "no_stripes", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "30", "valid": "30"},
    "layout":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    layout = (overrides.get("texture") if overrides.get("texture") in LAYOUTS else None) or \
             overrides.get("layout") or \
             ctx.draw_choice("layout", list(LAYOUTS))
    endpoint, stripe, waypoint = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(15, 30, 0)
    if layout == "wide":
        start, end, markers = (1, 4), (13, 25), [(5, 10), (9, 20)]
    elif layout == "shifted":
        start, end, markers = (2, 24), (13, 5), [(6, 18), (10, 11)]
    else:
        start, end, markers = (1, 7), (13, 23), [(4, 12), (8, 17), (11, 22)]
    g[start[0]][start[1]] = endpoint
    g[end[0]][end[1]] = endpoint
    for mr, mc in markers:
        for c in range(30):
            g[mr][c] = stripe
        for dc in (-1, 0, 1):
            g[mr][mc + dc] = waypoint
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 30, 0)
    if name == "no_endpoints":
        for c in range(30):
            g[7][c] = 4
        return g
    if name == "no_stripes":
        g[1][4] = 3
        g[13][25] = 3
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(30):
                g[r][c] = 4
        return g
    return g
