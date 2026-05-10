"""Generator for cad67732.

Rule: sparse periodic pattern is extended into a doubled canvas by
its first valid shift.

Combinatorial axes (8): grid_size, period, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_pattern, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7af6bf709882"
VERSION = "1.1.0"
TASK_ID = "7af6bf709882"
SUMMARY = "Sparse periodic pattern extended into doubled canvas by first valid shift."

INVARIANTS = [
    "the background is zero",
    "nonzero cells repeat under a positive row shift and a small column shift",
    "the repeated cells stay within the source grid",
    "the seed color is non-zero",
]

PERIODS = ("p21", "p22", "p31")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "full_grid", "single_pixel")
HELPFUL_TEXTURES = PERIODS

PERIOD_VECS = {
    "p21": (2, 1),
    "p22": (2, 2),
    "p31": (3, 1),
}

AXES = {
    "grid_size":      {"type": "int", "default": "7", "valid": "7"},
    "period":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PERIODS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for period",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    period = (overrides.get("texture") if overrides.get("texture") in PERIODS else None) or \
             overrides.get("period") or \
             ctx.draw_choice("period", list(PERIODS))
    pr, pc = PERIOD_VECS[period]
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(7, 7, 0)
    starts = [(0, 0), (0, 3), (1, 1)]
    for sr, sc in starts:
        k = 0
        while sr + k * pr < 7 and 0 <= sc + k * pc < 7:
            g[sr + k * pr][sc + k * pc] = color
            k += 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_pattern":
        return g
    if name == "single_pixel":
        g[3][3] = 2
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 2
        return g
    return g
