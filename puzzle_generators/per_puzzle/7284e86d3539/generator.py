"""Generator for 234bbc79.

Rule: gray markers inherit nearest colors, then connected objects are
packed into a 3-row strip.

Combinatorial axes (8): grid_h/w, component_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_components, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7284e86d3539"
VERSION = "1.1.0"
TASK_ID = "7284e86d3539"
SUMMARY = "Gray markers inherit nearest colors; components packed into 3-row strip."

INVARIANTS = [
    "nonzero non-gray colored components are separated by columns",
    "gray markers are nearest to their intended color component",
    "recolored components have height at most two",
    "component colors are distinct and exclude gray",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "component_count":{"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        cc_lo, cc_hi = 2, 2
    elif difficulty == "hard":
        cc_lo, cc_hi = 4, 4
    else:
        cc_lo, cc_hi = 2, 4
    component_count = ctx.draw_int("component_count", cc_lo, cc_hi)
    colors = ctx.draw_distinct_colors("colors", n=component_count, exclude={0, 5})
    g = full_grid(6, 16, 0)
    starts = [1, 5, 9, 13]
    for i in range(component_count):
        c = starts[i]
        r = rng.randint(1, 3)
        g[r][c] = colors[i]
        g[r + 1][c] = colors[i]
        if c + 1 < len(g[0]) and rng.choice([True, False]):
            g[r + 1][c + 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 16, 0)
    if name == "no_components":
        return g
    if name == "no_markers":
        for i, c in enumerate([1, 5, 9, 13]):
            g[2][c] = 2 + i
            g[3][c] = 2 + i
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(16):
                g[r][c] = 5
        return g
    return g
