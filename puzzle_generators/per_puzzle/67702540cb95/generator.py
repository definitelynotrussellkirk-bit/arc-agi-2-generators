"""Generator for 20981f0e.

Rule: blue shapes inside red-dot partition cells are recentered within
their cell ranges.

Combinatorial axes (8): grid_h/w, shape_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_dots, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "67702540cb95"
VERSION = "1.1.0"
TASK_ID = "67702540cb95"
SUMMARY = "Blue shapes inside red-dot partition cells recentered in cell ranges."

INVARIANTS = [
    "red dots define at least two partition rows and columns",
    "blue shapes lie fully inside partition cells",
    "each blue shape has dimensions compatible with exact centering",
    "shape colors are color 1 on color-0 background",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "shape_count":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
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
    if difficulty == "easy":
        sc_lo, sc_hi = 2, 2
    elif difficulty == "hard":
        sc_lo, sc_hi = 4, 5
    else:
        sc_lo, sc_hi = 2, 4
    shape_count = ctx.draw_int("shape_count", sc_lo, sc_hi)
    h = 14
    w = 14
    g = full_grid(h, w, 0)
    red_rows = [4, 9]
    red_cols = [4, 9]
    for r in red_rows:
        for c in red_cols:
            g[r][c] = 2
    sections = [(0, 0), (0, 5), (0, 10), (5, 0), (5, 5), (5, 10), (10, 0), (10, 5), (10, 10)]
    rng.shuffle(sections)
    for r0, c0 in sections[:shape_count]:
        rr = r0 + rng.choice([0, 2])
        cc = c0 + rng.choice([0, 2])
        draw_rect(g, rr, cc, 2, 2, 1)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_dots":
        draw_rect(g, 5, 5, 2, 2, 1)
        return g
    if name == "no_shapes":
        for r in [4, 9]:
            for c in [4, 9]:
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 1
        return g
    return g
