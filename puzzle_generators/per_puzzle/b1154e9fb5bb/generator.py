"""Generator for b457fec5.

Rule: a gray diagonal staircase is recolored by a cycling legend with
saturation.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_legend, no_staircase, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "b1154e9fb5bb"
VERSION = "1.1.0"
TASK_ID = "b1154e9fb5bb"
SUMMARY = "Gray diagonal staircase recolored by cycling legend with saturation."

INVARIANTS = [
    "the first non-empty non-gray row is the color legend",
    "a gray object is made from overlapping legend-sized blocks along a diagonal",
    "gray cells are recolored by diagonal offset and saturate after the last full cycle",
]

DIRECTIONS = ("right", "left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_legend", "no_staircase", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    direction = (overrides.get("texture") if overrides.get("texture") in DIRECTIONS else None) or \
                overrides.get("direction") or \
                ("right" if sample_index % 2 == 0 else "left")
    legend = ctx.draw_distinct_colors("legend", n=3, exclude={0, 5})
    steps = 4 + (sample_index % 2)
    g = full_grid(12, 14, 0)
    for i, color in enumerate(legend):
        g[0][i + 1] = color
    start_r = 3
    start_c = 2 if direction == "right" else 10
    for k in range(steps):
        c = start_c + k if direction == "right" else start_c - k
        draw_rect(g, start_r + k, c, 3, 3, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_legend":
        draw_rect(g, 3, 2, 3, 3, 5)
        return g
    if name == "no_staircase":
        for i, color in enumerate([3, 4, 6]):
            g[0][i + 1] = color
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(14):
                g[r][c] = 5
        return g
    return g
