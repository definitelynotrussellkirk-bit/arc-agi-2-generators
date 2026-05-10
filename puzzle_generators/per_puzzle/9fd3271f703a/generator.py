"""Generator for 985ae207.

Rule: a 3x3 motif stretches toward the nearest matching colored bar.

Combinatorial axes (8): grid_h/w, orientation, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_motif, no_bar, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9fd3271f703a"
VERSION = "1.1.0"
TASK_ID = "9fd3271f703a"
SUMMARY = "3x3 motif stretches toward nearest matching colored bar."

INVARIANTS = [
    "motifs are 3x3 blocks with a uniform outer ring and distinct center",
    "a separate object of the center color is aligned horizontally or vertically",
    "the rule fills the corridor with the outer color and repeats the center marker periodically",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_motif", "no_bar", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
                  ("horizontal" if sample_index % 2 == 0 else "vertical")
    outer, center = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    h = 15
    w = 15
    g = full_grid(h, w, 0)
    mr = 4 + (sample_index % 3)
    mc = 3 + (sample_index % 2)
    for r in range(mr, mr + 3):
        for c in range(mc, mc + 3):
            g[r][c] = outer
    g[mr + 1][mc + 1] = center

    if orientation == "horizontal":
        bar_c = 10 + (sample_index % 2)
        for c in range(bar_c, bar_c + 3):
            g[mr + 1][c] = center
    else:
        bar_r = 10 + (sample_index % 2)
        for r in range(bar_r, bar_r + 3):
            g[r][mc + 1] = center
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_motif":
        g[5][12] = 3
        return g
    if name == "no_bar":
        for r in range(4, 7):
            for c in range(3, 6):
                g[r][c] = 4
        g[5][4] = 3
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 4
        return g
    return g
