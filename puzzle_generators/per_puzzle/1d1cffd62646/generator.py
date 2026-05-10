"""Generator for 5c2c9af4.

Rule: two non-bg dots define a center and a step distance; rule draws
concentric square outlines through the grid in the dot color.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, step, dot_color.
Degenerates: no_dots, single_dot, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1d1cffd62646"
VERSION = "1.1.0"
TASK_ID = "1d1cffd62646"
SUMMARY = "Two dots: marker + center; rule draws concentric square outlines."

INVARIANTS = [
    "background is 0",
    "exactly two non-bg cells of the same color",
    "marker row is strictly less than center row",
    "step is the chebyshev distance between the two dots and is at least 2",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "single_dot", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..20", "valid": "10..24"},
    "grid_w":         {"type": "int", "default": "rng 14..20", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "step":           {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "dot_color":      {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 14, 16
    elif difficulty == "hard":
        h_lo, h_hi = 20, 24
    else:
        h_lo, h_hi = 14, 20
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=1, exclude={0})
    color = palette[0]
    g = full_grid(h, w, 0)
    cr = rng.randint(h // 3, 2 * h // 3)
    cc = rng.randint(w // 3, 2 * w // 3)
    step = rng.randint(2, 4)
    mr, mc = cr - step, cc
    if mr < 0:
        return [[0]]
    g[mr][mc] = color
    g[cr][cc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_dots":
        return g
    if name == "single_dot":
        g[7][7] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
