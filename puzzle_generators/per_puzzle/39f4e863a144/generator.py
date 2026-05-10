"""Generator for f1cefba8.

Rule: inner tab protrusions cut through the inner object and extend
outward through the outer frame.

Combinatorial axes (8): grid_h/w, tab_axis, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_outer, no_inner, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, draw_rect, full_grid

GENERATOR_ID = "39f4e863a144"
VERSION = "1.1.0"
TASK_ID = "39f4e863a144"
SUMMARY = "Inner tab protrusions cut through inner object and extend through outer frame."

INVARIANTS = [
    "the background is zero",
    "the largest bbox object is the outer frame",
    "the second largest bbox object is an inner object with one-cell tabs on its edge",
    "outer and inner colors are distinct and non-zero",
]

TAB_AXES = ("row", "col")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_outer", "no_inner", "full_grid")
HELPFUL_TEXTURES = TAB_AXES

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "tab_axis":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TAB_AXES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for tab_axis",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    axis = (overrides.get("texture") if overrides.get("texture") in TAB_AXES else None) or \
           overrides.get("tab_axis") or \
           ctx.draw_choice("tab_axis", list(TAB_AXES))
    outer, inner = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(13, 13, 0)
    draw_frame(g, 2, 2, 10, 10, outer)
    draw_rect(g, 5, 5, 3, 3, inner)
    if axis == "row":
        g[6][4] = inner
        g[6][8] = inner
    else:
        g[4][6] = inner
        g[8][6] = inner
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_outer":
        draw_rect(g, 5, 5, 3, 3, 2)
        return g
    if name == "no_inner":
        draw_frame(g, 2, 2, 10, 10, 1)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 1
        return g
    return g
